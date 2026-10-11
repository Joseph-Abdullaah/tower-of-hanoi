"""Everything that talks to Node, pnpm and Remotion (SRS §6, §7).

This is the only file that knows how the video is made.
"""

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from hanoi import config
from hanoi.models import Move, RenderOptions

COMPOSITION_ID = "Hanoi"
ERROR_TAIL_LINES = 15

_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


class RenderError(Exception):
    """A problem the user should see: missing tools, a failed render, a file that can't be written."""

    def __init__(self, message: str, details: Sequence[str] = ()) -> None:
        super().__init__(message)
        self.message = message
        self.details = list(details)


def check_requirements() -> None:
    """Make sure Node.js, pnpm and the Remotion packages are installed (FR-8)."""
    if shutil.which("node") is None:
        raise RenderError("Node.js is not installed. See README → Prerequisites.")
    if shutil.which("pnpm") is None:
        raise RenderError("pnpm is not installed. See README → Prerequisites.")
    if not (config.VIDEO_PROJECT_DIR / "node_modules").is_dir():
        raise RenderError("Remotion dependencies are not installed. Run `cd video && pnpm install`.")


def output_path(options: RenderOptions) -> Path:
    """videos/hanoi_<n>disks_<speed>_<sd|hd>.mp4 (FR-27)."""
    quality = config.QUALITY_LABEL[options.quality]
    return config.VIDEOS_DIR / f"hanoi_{options.disks}disks_{options.speed}_{quality}.mp4"


def build_props(options: RenderOptions, moves: Sequence[Move]) -> dict[str, Any]:
    """The props contract from SRS §3.3. Every timing number comes from config.py."""
    return {
        "disks": options.disks,
        "speed": options.speed,
        "fps": config.FPS,
        "framesPerMove": config.FRAMES_PER_MOVE[options.speed],
        "introFrames": config.INTRO_FRAMES,
        "endPauseFrames": config.END_PAUSE_FRAMES,
        "outroFrames": config.OUTRO_FRAMES,
        "totalMoves": len(moves),
        "moves": [{"number": m.number, "disk": m.disk, "from": m.source, "to": m.target} for m in moves],
    }


def write_props(props: dict[str, Any]) -> Path:
    """Write the props to .cache/props.json and return its path."""
    try:
        config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        config.PROPS_FILE.write_text(json.dumps(props, indent=2), encoding="utf-8")
    except OSError as e:
        raise RenderError(f"Can't write {config.PROPS_FILE.name}: {e.strerror or e}") from e
    return config.PROPS_FILE


def render(options: RenderOptions, moves: Sequence[Move]) -> tuple[Path, float]:
    """Render the video with Remotion. Returns the video path and how long it took in seconds.

    Raises RenderError if the render fails. On Ctrl+C the render is stopped before the
    KeyboardInterrupt carries on up to the app.
    """
    props_file = write_props(build_props(options, moves))
    video = output_path(options)
    try:
        video.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise RenderError(f"Can't write to {video.parent.name}/: {e.strerror or e}") from e

    pnpm = shutil.which("pnpm")
    if pnpm is None:
        raise RenderError("pnpm is not installed. See README → Prerequisites.")
    command = [
        pnpm,  # on Windows this is pnpm.cmd, which works with a list of arguments
        "exec",
        "remotion",
        "render",
        "src/index.ts",
        COMPOSITION_ID,
        str(video),
        f"--props={props_file}",
        f"--scale={config.QUALITY_SCALE[options.quality]:g}",
    ]

    start = time.perf_counter()
    try:
        # Output goes to a log file (not a pipe) so we can poll the process below
        with config.RENDER_LOG.open("w", encoding="utf-8") as log:
            process = subprocess.Popen(
                command,
                cwd=config.VIDEO_PROJECT_DIR,
                stdout=log,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                env={**os.environ, "FORCE_COLOR": "0", "NO_COLOR": "1"},
                **_own_process_group(),
            )
            try:
                _wait(process)
            except KeyboardInterrupt:
                _stop(process)
                raise
    except OSError as e:
        raise RenderError(f"Couldn't run the render: {e.strerror or e}") from e
    seconds = time.perf_counter() - start

    if process.returncode != 0:
        output = config.RENDER_LOG.read_text(encoding="utf-8", errors="replace")
        lines = [_ANSI.sub("", line).rstrip() for line in output.splitlines()]
        tail = [line for line in lines if line.strip()][-ERROR_TAIL_LINES:]
        log_path = config.RENDER_LOG.relative_to(config.PROJECT_ROOT).as_posix()
        raise RenderError("Render failed.", [*tail, "", f"Full log: {log_path}"])
    return video, seconds


def _wait(process: subprocess.Popen[bytes]) -> None:
    """Wait in short steps: a single long wait can't be interrupted by Ctrl+C on Windows."""
    while True:
        try:
            process.wait(timeout=0.2)
            return
        except subprocess.TimeoutExpired:
            continue


def _own_process_group() -> dict[str, Any]:
    """Start the render in its own process group so Ctrl+C reaches only Python, which then stops it."""
    if sys.platform == "win32":
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def _stop(process: subprocess.Popen[bytes]) -> None:
    """Stop the render and everything it started (pnpm → node → headless browser)."""
    if process.poll() is not None:
        return
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(process.pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
