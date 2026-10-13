import { BASE, HUD_Y, ROD_X, RODS, diskY } from "../lib/layout";
import { COLORS } from "../lib/theme";
import type { FrameState } from "../lib/timeline";
import type { HanoiProps } from "../types";
import { Base } from "./Base";
import { Disk } from "./Disk";
import { MoveLabel } from "./MoveLabel";
import { Rod } from "./Rod";

type SceneProps = { props: HanoiProps; state: FrameState };

/** Title line, rods, base, every disk and the move label for one frame. */
export const Scene: React.FC<SceneProps> = ({ props, state }) => (
  <>
    <div
      style={{
        position: "absolute",
        left: BASE.left,
        top: HUD_Y,
        width: BASE.width,
        display: "flex",
        justifyContent: "space-between",
        fontSize: 20,
      }}
    >
      <span style={{ color: COLORS.amber }}>TOWER OF HANOI</span>
      <span style={{ color: COLORS.dim }}>
        {`${props.disks} ${props.disks === 1 ? "DISK" : "DISKS"} · ${props.speed.toUpperCase()}`}
      </span>
    </div>

    {RODS.map((rod) => (
      <Rod key={rod} rod={rod} />
    ))}
    <Base />

    {RODS.map((rod) =>
      state.stacks[rod].map((disk, level) => (
        <Disk key={disk} disk={disk} disks={props.disks} x={ROD_X[rod]} y={diskY(level)} />
      )),
    )}
    {state.moving ? (
      <Disk
        key={state.moving.disk}
        disk={state.moving.disk}
        disks={props.disks}
        x={state.moving.x}
        y={state.moving.y}
      />
    ) : null}

    <MoveLabel move={state.labelMove} total={props.totalMoves} />
  </>
);
