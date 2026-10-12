// Props contract with Python (SRS §3.3). Python writes these to .cache/props.json.

export type Rod = "A" | "B" | "C";

export type Move = { number: number; disk: number; from: Rod; to: Rod };

export type HanoiProps = {
  disks: number;
  speed: "slow" | "normal" | "fast";
  fps: number;
  framesPerMove: number;
  introFrames: number;
  endPauseFrames: number;
  outroFrames: number;
  totalMoves: number;
  moves: Move[];
};
