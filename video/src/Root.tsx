import { CalculateMetadataFunction, Composition } from "remotion";
import { HanoiVideo } from "./HanoiVideo";
import { HEIGHT, WIDTH } from "./lib/layout";
import type { HanoiProps } from "./types";

// Sample for Remotion Studio and `pnpm render` only (3 disks, normal), generated from the Python
// solver + config.py. Real renders get every value from Python via --props.
const sampleProps: HanoiProps = {
  disks: 3,
  speed: "normal",
  fps: 30,
  framesPerMove: 24,
  introFrames: 60,
  endPauseFrames: 30,
  outroFrames: 90,
  totalMoves: 7,
  moves: [
    { number: 1, disk: 1, from: "A", to: "C" },
    { number: 2, disk: 2, from: "A", to: "B" },
    { number: 3, disk: 1, from: "C", to: "B" },
    { number: 4, disk: 3, from: "A", to: "C" },
    { number: 5, disk: 1, from: "B", to: "A" },
    { number: 6, disk: 2, from: "B", to: "C" },
    { number: 7, disk: 1, from: "A", to: "C" },
  ],
};

// Video length comes from the props (FR-18)
const calculateMetadata: CalculateMetadataFunction<HanoiProps> = ({ props }) => ({
  durationInFrames: props.introFrames + props.totalMoves * props.framesPerMove + props.endPauseFrames + props.outroFrames,
  fps: props.fps,
});

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Hanoi"
    component={HanoiVideo}
    width={WIDTH}
    height={HEIGHT}
    fps={sampleProps.fps}
    durationInFrames={1} // replaced by calculateMetadata
    defaultProps={sampleProps}
    calculateMetadata={calculateMetadata}
  />
);
