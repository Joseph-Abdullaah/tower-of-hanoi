"""All constants for the app: the single source of truth (SRS §3.2).

Python sends the frame values to Remotion inside the props, so the video
project never keeps its own copy of these numbers.
"""

from pathlib import Path
from typing import Final

from hanoi.models import Quality, Speed

# Puzzle limits
MIN_DISKS: Final = 1
MAX_DISKS: Final = 7

# Video timing (frames at FPS)
FPS: Final = 30
FRAMES_PER_MOVE: Final[dict[Speed, int]] = {
    "slow": 45,  # 1.5s
    "normal": 24,  # 0.8s
    "fast": 12,  # 0.4s
}
INTRO_FRAMES: Final = 60  # 2s
END_PAUSE_FRAMES: Final = 30  # 1s
OUTRO_FRAMES: Final = 90  # 3s

# Video quality: Remotion --scale on the 1280x720 composition
QUALITY_SCALE: Final[dict[Quality, float]] = {
    "low": 1,  # 1280x720
    "high": 1.5,  # 1920x1080
}
QUALITY_LABEL: Final[dict[Quality, str]] = {"low": "sd", "high": "hd"}  # used in file names
COMPOSITION_WIDTH: Final = 1280  # must match the Hanoi composition in video/src/Root.tsx
COMPOSITION_HEIGHT: Final = 720

# Menu defaults (FR-5)
DEFAULT_SPEED: Final[Speed] = "normal"
DEFAULT_QUALITY: Final[Quality] = "low"

# Paths (src/hanoi/config.py -> project root is two folders up)
PROJECT_ROOT: Final = Path(__file__).resolve().parents[2]
VIDEO_PROJECT_DIR: Final = PROJECT_ROOT / "video"
CACHE_DIR: Final = PROJECT_ROOT / ".cache"
PROPS_FILE: Final = CACHE_DIR / "props.json"
RENDER_LOG: Final = CACHE_DIR / "render.log"  # full Remotion output from the last render
VIDEOS_DIR: Final = PROJECT_ROOT / "videos"
