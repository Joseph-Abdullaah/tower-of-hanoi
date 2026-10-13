import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { COLORS } from "../lib/theme";

type OutroProps = { disks: number; totalMoves: number; durationInFrames: number };

/** Drawn tick: the pixel font has no ✓ glyph. */
const CheckMark: React.FC = () => (
  <svg width={34} height={34} viewBox="0 0 34 34" style={{ marginLeft: 20 }}>
    <polyline
      points="4,18 13,27 30,8"
      fill="none"
      stroke={COLORS.green}
      strokeWidth={6}
      strokeLinecap="square"
    />
  </svg>
);

/** "SOLVED!" + "15 MOVES = 2⁴ − 1 ✓" card. */
export const OutroCard: React.FC<OutroProps> = ({ disks, totalMoves, durationInFrames }) => {
  const frame = useCurrentFrame();
  const fade = Math.max(1, Math.round(durationInFrames / 3));
  const opacity = interpolate(frame, [0, fade], [0, 1], { extrapolateRight: "clamp" });
  const scale = interpolate(frame, [0, fade], [0.9, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        opacity,
        background: COLORS.background,
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        gap: 56,
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          fontSize: 72,
          color: COLORS.amber,
          textShadow: `4px 4px 0 ${COLORS.amberDeep}, 8px 8px 0 ${COLORS.amberShadow}`,
        }}
      >
        SOLVED!
      </div>
      <div style={{ display: "flex", alignItems: "center", fontSize: 30, color: COLORS.cream, whiteSpace: "pre" }}>
        {`${totalMoves} ${totalMoves === 1 ? "MOVE" : "MOVES"} = 2`}
        <span style={{ fontSize: 18, position: "relative", top: -14, marginLeft: 2 }}>{disks}</span>
        {/* The font has no "−" glyph; its "-" looks the same in pixel style */}
        {" - 1"}
        <CheckMark />
      </div>
    </AbsoluteFill>
  );
};
