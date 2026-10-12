// Frame → where every disk is (SRS §5.2). Components only draw what this returns.
import { Easing, interpolate } from "remotion";
import type { HanoiProps, Move, Rod } from "../types";
import { diskY, LIFT_Y, ROD_X } from "./layout";

/** Disks on each rod, bottom → top. */
export type Stacks = Record<Rod, number[]>;

export type MovingDisk = { disk: number; x: number; y: number };

export type FrameState = {
  stacks: Stacks; // resting disks (the moving disk is not included)
  moving: MovingDisk | null;
  labelMove: Move | null; // move shown in the label; null before the first move
};

// Each move: lift 30% → slide 40% → drop 30%
const LIFT_END = 0.3;
const SLIDE_END = 0.7;
const ease = { easing: Easing.inOut(Easing.cubic), extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** states[k] = stacks before move k; states[moves.length] = final stacks. Built once per video. */
export const buildStates = (disks: number, moves: Move[]): Stacks[] => {
  let current: Stacks = { A: [], B: [], C: [] };
  for (let disk = disks; disk >= 1; disk--) {
    current.A.push(disk);
  }
  const states: Stacks[] = [current];
  for (const move of moves) {
    const next: Stacks = { A: [...current.A], B: [...current.B], C: [...current.C] };
    const disk = next[move.from].pop();
    if (disk === undefined) {
      throw new Error(`Move ${move.number}: rod ${move.from} is empty`);
    }
    next[move.to].push(disk);
    states.push(next);
    current = next;
  }
  return states;
};

export const getFrameState = (frame: number, props: HanoiProps, states: Stacks[]): FrameState => {
  const total = props.moves.length;
  const f = frame - props.introFrames;
  if (f < 0 || total === 0) {
    return { stacks: states[0], moving: null, labelMove: null };
  }

  const k = Math.floor(f / props.framesPerMove);
  if (k >= total) {
    return { stacks: states[total], moving: null, labelMove: props.moves[total - 1] };
  }

  const move = props.moves[k];
  const before = states[k];
  // Progress in (0, 1]: the last frame of a move lands exactly, so nothing snaps into place
  const p = ((f % props.framesPerMove) + 1) / props.framesPerMove;

  const startY = diskY(before[move.from].length - 1);
  const endY = diskY(before[move.to].length);
  const fromX = ROD_X[move.from];
  const toX = ROD_X[move.to];

  let x: number;
  let y: number;
  if (p <= LIFT_END) {
    x = fromX;
    y = interpolate(p, [0, LIFT_END], [startY, LIFT_Y], ease);
  } else if (p <= SLIDE_END) {
    x = interpolate(p, [LIFT_END, SLIDE_END], [fromX, toX], ease);
    y = LIFT_Y;
  } else {
    x = toX;
    y = interpolate(p, [SLIDE_END, 1], [LIFT_Y, endY], ease);
  }

  const stacks: Stacks = { ...before, [move.from]: before[move.from].slice(0, -1) };
  return { stacks, moving: { disk: move.disk, x, y }, labelMove: move };
};
