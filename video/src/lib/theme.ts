// Colors and font. Same amber CRT palette as the Python CLI (src/hanoi/ui.py).
import { cancelRender, continueRender, delayRender, staticFile } from "remotion";

export const COLORS = {
  background: "#100d08",
  backgroundGlow: "#221a0e",
  amber: "#ffb000",
  amberDeep: "#ff7a00",
  amberShadow: "#5a2c00",
  cream: "#ffe7a8",
  dim: "#8a7550",
  rod: "#6e5733",
  rodHighlight: "#9c7f4a",
  base: "#4a3920",
  baseEdge: "#ffb000",
  green: "#3ddc84",
  diskText: "#1a1309",
};

// One color per disk size, smallest first (matches the CLI moves table)
export const DISK_COLORS = ["#ff4d3d", "#ff9f1c", "#ffd23f", "#3ddc84", "#3fa7ff"];

export const diskColor = (disk: number): string => DISK_COLORS[(disk - 1) % DISK_COLORS.length];

// ── Font: Press Start 2P, bundled in public/fonts so rendering works offline ──
export const FONT_FAMILY = "Press Start 2P";

const fontHandle = delayRender("Loading Press Start 2P font");
const font = new FontFace(
  FONT_FAMILY,
  `url('${staticFile("fonts/PressStart2P-Regular.ttf")}') format('truetype')`,
);
font
  .load()
  .then(() => {
    document.fonts.add(font);
    continueRender(fontHandle);
  })
  .catch((err: unknown) => cancelRender(err));
