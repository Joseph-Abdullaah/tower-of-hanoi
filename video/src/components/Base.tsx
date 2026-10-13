import { BASE } from "../lib/layout";
import { COLORS } from "../lib/theme";

/** The platform the rods stand on. */
export const Base: React.FC = () => (
  <div
    style={{
      position: "absolute",
      left: BASE.left,
      top: BASE.top,
      width: BASE.width,
      height: BASE.height,
      borderRadius: 8,
      background: COLORS.base,
      borderTop: `4px solid ${COLORS.baseEdge}`,
      boxShadow: `0 0 28px ${COLORS.amber}33, 0 10px 0 #00000080`,
    }}
  />
);
