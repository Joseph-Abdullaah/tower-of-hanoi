import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { COLORS } from "../lib/theme";
import type { HanoiProps } from "../types";

type IntroProps = { disks: number; speed: HanoiProps["speed"]; durationInFrames: number };

/** "TOWER OF HANOI" title card that pops in, then fades into the scene. */
export const IntroCard: React.FC<IntroProps> = ({ disks, speed, durationInFrames }) => {
  const frame = useCurrentFrame();
  const fade = Math.max(1, Math.round(durationInFrames / 3));
  const opacity = interpolate(frame, [durationInFrames - fade, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
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
          fontSize: 60,
          color: COLORS.amber,
          textShadow: `4px 4px 0 ${COLORS.amberDeep}, 8px 8px 0 ${COLORS.amberShadow}`,
        }}
      >
        TOWER OF HANOI
      </div>
      <div style={{ fontSize: 24, color: COLORS.cream }}>
        {`${disks} ${disks === 1 ? "DISK" : "DISKS"} · ${speed.toUpperCase()}`}
      </div>
    </AbsoluteFill>
  );
};
