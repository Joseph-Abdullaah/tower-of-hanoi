// Positions and sizes on the 1280×720 composition (SRS §5.3).
import type { Rod } from "../types";

export const WIDTH = 1280;
export const HEIGHT = 720;

export const ROD_X: Record<Rod, number> = { A: 320, B: 640, C: 960 };
export const RODS: Rod[] = ["A", "B", "C"];

export const BASE = { left: 110, width: 1060, top: 520, height: 26 };
export const ROD = { width: 18, height: 262 }; // tall enough for 5 disks with room above
export const ROD_TOP = BASE.top - ROD.height;

export const DISK_HEIGHT = 34;
export const DISK_GAP = 6;
const DISK_MIN_WIDTH = 90;
const DISK_MAX_WIDTH = 280;
const SINGLE_DISK_WIDTH = 200;

// Centre y of a disk while it slides between rods: clearly above the rod tops
export const LIFT_Y = ROD_TOP - 26 - DISK_HEIGHT / 2;

export const ROD_LABEL_Y = BASE.top + BASE.height + 20; // top of the A / B / C labels
export const MOVE_LABEL_Y = 636; // top of the move label
export const HUD_Y = 48; // top of the title line

/** Centre y of a disk resting at `level` in a stack (0 = bottom). */
export const diskY = (level: number): number =>
  BASE.top - DISK_HEIGHT / 2 - level * (DISK_HEIGHT + DISK_GAP);

/** Disk widths spread evenly from smallest to largest, so 1 and 5 disks both look good. */
export const diskWidth = (disk: number, disks: number): number => {
  if (disks <= 1) {
    return SINGLE_DISK_WIDTH;
  }
  return DISK_MIN_WIDTH + ((disk - 1) * (DISK_MAX_WIDTH - DISK_MIN_WIDTH)) / (disks - 1);
};
