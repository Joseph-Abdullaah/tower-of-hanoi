import { ROD, ROD_LABEL_Y, ROD_TOP, ROD_X } from "../lib/layout";
import { COLORS } from "../lib/theme";
import type { Rod as RodName } from "../types";

/** One rounded rod plus its A / B / C label under the base. */
export const Rod: React.FC<{ rod: RodName }> = ({ rod }) => {
  const x = ROD_X[rod];
  return (
    <>
      <div
        style={{
          position: "absolute",
          left: x - ROD.width / 2,
          top: ROD_TOP,
          width: ROD.width,
          height: ROD.height + 4, // tucks under the base edge
          borderRadius: `${ROD.width / 2}px ${ROD.width / 2}px 0 0`,
          background: `linear-gradient(to right, ${COLORS.rodHighlight}, ${COLORS.rod})`,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: x - 40,
          top: ROD_LABEL_Y,
          width: 80,
          textAlign: "center",
          fontSize: 28,
          color: COLORS.amber,
          textShadow: `0 0 12px ${COLORS.amber}88`,
        }}
      >
        {rod}
      </div>
    </>
  );
};
