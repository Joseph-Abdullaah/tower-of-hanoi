"""Main loop: menu routing, input validation and the solve → render flow."""

from typing import Literal

from hanoi import config, renderer, ui
from hanoi.engine import IllegalMoveError, verify_solution
from hanoi.models import QUALITIES, SPEEDS, Move, RenderOptions
from hanoi.solver import solve

NextStep = Literal["main", "quit"]


def main() -> None:
    """Entry point for `uv run hanoi`."""
    try:
        _main_menu()
    except (KeyboardInterrupt, EOFError):  # Ctrl+C (or Ctrl+Z / Ctrl+D) anywhere: exit cleanly (FR-12)
        pass
    ui.goodbye()


def _main_menu() -> None:
    while True:
        ui.show_home()
        choice = _ask_choice("Choose an option", 4)
        if choice == 1:
            if _solve_flow() == "quit":
                return
        elif choice == 2:
            ui.show_rules()
            ui.wait_for_enter()
        elif choice == 3:
            ui.show_about()
            ui.wait_for_enter()
        else:
            return


def _solve_flow() -> NextStep:
    """Disks → speed → quality → summary → solve → render → after-render menu."""
    disks: int | None = None
    while True:
        ui.show_solve_header()
        if disks is None:
            disks = _ask_disks()
        else:
            ui.info(f"Same puzzle: {disks} disks")

        ui.show_speed_menu()
        speed = SPEEDS[_ask_choice("Choose a speed", len(SPEEDS), SPEEDS.index(config.DEFAULT_SPEED) + 1) - 1]
        ui.show_quality_menu()
        quality = QUALITIES[
            _ask_choice("Choose a quality", len(QUALITIES), QUALITIES.index(config.DEFAULT_QUALITY) + 1) - 1
        ]
        options = RenderOptions(disks=disks, speed=speed, quality=quality)

        ui.show_summary(options, min_moves=2**disks - 1, video_seconds=_estimated_seconds(options))
        if not _ask_yes_no("Start rendering?"):
            return "main"

        try:
            renderer.check_requirements()
        except renderer.RenderError as e:
            ui.error_panel("MISSING REQUIREMENT", e.message)
            ui.wait_for_enter()
            return "main"

        moves = solve(disks)
        if not _solution_is_valid(disks, moves):
            ui.wait_for_enter()
            return "main"
        ui.show_moves(moves, disks)

        try:
            with ui.rendering():
                path, seconds = renderer.render(options, moves)
            ui.show_render_success(path.relative_to(config.PROJECT_ROOT).as_posix(), seconds)
        except renderer.RenderError as e:
            ui.error_panel("RENDER FAILED", e.message, e.details)

        ui.show_after_render_menu()
        choice = _ask_choice("What next?", 4)
        if choice == 2:
            disks = None
        elif choice == 3:
            return "main"
        elif choice == 4:
            return "quit"


# ── Input validation ──


def _parse_in_range(raw: str, low: int, high: int) -> int | None:
    """The whole number in raw if it's between low and high, otherwise None."""
    raw = raw.strip()
    if raw.isascii() and raw.isdigit() and low <= int(raw) <= high:
        return int(raw)
    return None


def _ask_choice(prompt: str, count: int, default: int | None = None) -> int:
    """Ask for a menu number 1..count. Empty input picks the default, if there is one."""
    hint = f"1–{count}" if default is None else f"1–{count}, Enter = {default}"
    while True:
        raw = ui.ask(f"{prompt} [{hint}]:")
        if not raw.strip() and default is not None:
            return default
        choice = _parse_in_range(raw, 1, count)
        if choice is not None:
            return choice
        ui.error(f"Please enter a number from 1 to {count}.")


def _ask_disks() -> int:
    low, high = config.MIN_DISKS, config.MAX_DISKS
    while True:
        disks = _parse_in_range(ui.ask(f"How many disks? [{low}–{high}]:"), low, high)
        if disks is not None:
            return disks
        ui.error(f"Please enter a whole number from {low} to {high}.")


def _ask_yes_no(prompt: str) -> bool:
    """Y/n question; Enter means yes."""
    while True:
        raw = ui.ask(f"{prompt} [Y/n]:").strip().lower()
        if raw in ("", "y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        ui.error("Please answer y or n.")


# ── Solve / render steps ──


def _solution_is_valid(disks: int, moves: list[Move]) -> bool:
    """Replay the moves through the engine before rendering (FR-16)."""
    try:
        if verify_solution(disks, moves):
            return True
        ui.error_panel("INTERNAL ERROR", "Internal error: the moves don't end with every disk on rod C.")
    except IllegalMoveError as e:
        ui.error_panel("INTERNAL ERROR", f"Internal error: illegal move #{e.move.number}.", [str(e)])
    return False


def _estimated_seconds(options: RenderOptions) -> int:
    """Video length, rounded to the nearest second (same formula as FR-18)."""
    frames = (
        config.INTRO_FRAMES
        + (2**options.disks - 1) * config.FRAMES_PER_MOVE[options.speed]
        + config.END_PAUSE_FRAMES
        + config.OUTRO_FRAMES
    )
    return int(frames / config.FPS + 0.5)
