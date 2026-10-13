import { MOVE_LABEL_Y, WIDTH } from "../lib/layout";
import { COLORS, diskColor } from "../lib/theme";
import type { Move } from "../types";

/** "MOVE 5 / 15 · DISK 1 · A → C". Before the first move: "MOVE 0 / 15". */
export const MoveLabel: React.FC<{ move: Move | null; total: number }> = ({ move, total }) => {
  // Pad the move number to the width of the total so the label doesn't shift when digits change
  const number = String(move ? move.number : 0).padStart(String(total).length, " ");
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        top: MOVE_LABEL_Y,
        width: WIDTH,
        textAlign: "center",
        fontSize: 22,
        color: COLORS.cream,
        whiteSpace: "pre",
      }}
    >
      <span style={{ color: COLORS.amber }}>{`MOVE ${number} / ${total}`}</span>
      {move ? (
        <>
          {" · "}
          <span style={{ color: diskColor(move.disk) }}>{`DISK ${move.disk}`}</span>
          {` · ${move.from} → ${move.to}`}
        </>
      ) : null}
    </div>
  );
};
