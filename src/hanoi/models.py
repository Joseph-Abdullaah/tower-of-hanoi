"""Data types shared across the app (SRS §3.1)."""

from dataclasses import dataclass
from typing import Literal, get_args

Rod = Literal["A", "B", "C"]
Speed = Literal["slow", "normal", "fast"]
Quality = Literal["low", "high"]

# All options in menu order
SPEEDS: tuple[Speed, ...] = get_args(Speed)
QUALITIES: tuple[Quality, ...] = get_args(Quality)


@dataclass(frozen=True)
class Move:
    number: int  # 1-based move number
    disk: int  # 1 = smallest, n = largest
    source: Rod
    target: Rod


@dataclass(frozen=True)
class RenderOptions:
    disks: int  # 1..5
    speed: Speed
    quality: Quality
