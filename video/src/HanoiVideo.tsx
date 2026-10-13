import { useMemo } from "react";
import { AbsoluteFill, Sequence, useCurrentFrame } from "remotion";
import { IntroCard } from "./components/IntroCard";
import { OutroCard } from "./components/OutroCard";
import { Scene } from "./components/Scene";
import { COLORS, FONT_FAMILY } from "./lib/theme";
import { buildStates, getFrameState } from "./lib/timeline";
import type { HanoiProps } from "./types";

/** Faint scanlines + vignette for the CRT look. */
const CrtOverlay: React.FC = () => (
  <AbsoluteFill
    style={{
      pointerEvents: "none",
      backgroundImage: [
        "repeating-linear-gradient(to bottom, #00000026 0px, #00000026 2px, transparent 2px, transparent 4px)",
        "radial-gradient(ellipse at center, transparent 55%, #00000099 100%)",
      ].join(", "),
    }}
  />
);

/** Intro → moves → end pause → outro. */
export const HanoiVideo: React.FC<HanoiProps> = (props) => {
  const frame = useCurrentFrame();
  // Replay the moves once; each frame is then a quick lookup
  const states = useMemo(() => buildStates(props.disks, props.moves), [props.disks, props.moves]);
  const state = getFrameState(frame, props, states);
  const outroStart = props.introFrames + props.totalMoves * props.framesPerMove + props.endPauseFrames;

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 60%, ${COLORS.backgroundGlow}, ${COLORS.background} 70%)`,
        fontFamily: `'${FONT_FAMILY}', monospace`,
      }}
    >
      <Scene props={props} state={state} />
      {props.introFrames > 0 ? (
        <Sequence durationInFrames={props.introFrames}>
          <IntroCard disks={props.disks} speed={props.speed} durationInFrames={props.introFrames} />
        </Sequence>
      ) : null}
      {props.outroFrames > 0 ? (
        <Sequence from={outroStart} durationInFrames={props.outroFrames}>
          <OutroCard disks={props.disks} totalMoves={props.totalMoves} durationInFrames={props.outroFrames} />
        </Sequence>
      ) : null}
      <CrtOverlay />
    </AbsoluteFill>
  );
};
