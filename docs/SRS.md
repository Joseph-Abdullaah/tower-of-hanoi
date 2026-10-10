# Software Requirements Specification (SRS) — tower-of-hanoi

**Last updated:** 2026-10-11
**Related docs:** PRD.md, TECH_STACK.md, PROJECT_STRUCTURE.md, PHASES.md

---

## 1. Purpose

This document describes **how** the system works: its parts, the data passed between them, the rules each part must follow, and how errors are handled. The PRD says *what* to build; this says *how it behaves*.

---

## 2. System architecture

```
┌───────────────────────────────────────────────┐
│                PYTHON CLI (src/hanoi)         │
│                                               │
│  ui.py ──▶ app.py (main loop / menus)         │
│                 │                             │
│                 ├─▶ solver.py  → list[Move]   │
│                 ├─▶ engine.py  → checks moves │
│                 └─▶ renderer.py               │
│                       │ writes .cache/props.json
│                       │ runs pnpm exec remotion render
└───────────────────────┼───────────────────────┘
                        ▼
┌───────────────────────────────────────────────┐
│             REMOTION PROJECT (video/)         │
│                                               │
│  index.ts → Root.tsx (Composition "Hanoi")    │
│      calculateMetadata → video length         │
│  HanoiVideo.tsx                               │
│      ├─ IntroCard                             │
│      ├─ Scene: Base, Rod ×3, Disk ×n          │
│      │         MoveLabel                      │
│      └─ OutroCard                             │
│  lib/timeline.ts → where every disk is at     │
│                    any frame                  │
└───────────────────────┬───────────────────────┘
                        ▼
              videos/hanoi_<n>disks_<speed>_<quality>.mp4
```

---

## 3. Data model

### 3.1 Python

```python
Rod = Literal["A", "B", "C"]

@dataclass(frozen=True)
class Move:
    number: int   # 1-based move number
    disk: int     # 1 = smallest, n = largest
    source: Rod
    target: Rod

@dataclass(frozen=True)
class RenderOptions:
    disks: int            # 1..5
    speed: Literal["slow", "normal", "fast"]
    quality: Literal["low", "high"]
```

### 3.2 Configuration constants (`config.py`) — single source of truth

| Constant | Value |
|---|---|
| `MIN_DISKS` / `MAX_DISKS` | 1 / 5 |
| `FPS` | 30 |
| `FRAMES_PER_MOVE` | slow 45 (1.5s), normal 24 (0.8s), fast 12 (0.4s) |
| `QUALITY_SCALE` | low 1 (1280×720), high 1.5 (1920×1080) |
| `QUALITY_LABEL` (for file names) | low `sd`, high `hd` |
| `INTRO_FRAMES` | 60 (2s) |
| `END_PAUSE_FRAMES` | 30 (1s) |
| `OUTRO_FRAMES` | 90 (3s) |

Python sends the frame values inside the props, so Remotion never has its own copy of these numbers.

### 3.3 Props contract (`.cache/props.json`) — Python → Remotion

```json
{
  "disks": 4,
  "speed": "normal",
  "fps": 30,
  "framesPerMove": 24,
  "introFrames": 60,
  "endPauseFrames": 30,
  "outroFrames": 90,
  "totalMoves": 15,
  "moves": [
    { "number": 1, "disk": 1, "from": "A", "to": "B" },
    { "number": 2, "disk": 2, "from": "A", "to": "C" }
  ]
}
```

Matching TypeScript type (`video/src/types.ts`):

```ts
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
```

---

## 4. Functional requirements

### 4.1 CLI

| ID | Requirement |
|---|---|
| FR-1 | On start, the app clears the screen and shows the retro banner and main menu. |
| FR-2 | Main menu accepts only `1`–`4`. Anything else shows a red error and re-prompts. |
| FR-3 | Rules and About screens display their content in Rich panels and return to the main menu on Enter. |
| FR-4 | Disk input accepts whole numbers 1–5 only. Letters, decimals, empty input, 0 and 6+ are rejected with a message that says the allowed range. |
| FR-5 | Speed and quality are chosen from numbered options (default: Normal, Low). |
| FR-6 | Before rendering, a summary panel shows: disks, minimum moves (2ⁿ − 1), speed, quality/resolution, estimated video length. User confirms with Y/n. |
| FR-7 | After confirming, the app solves the puzzle and prints a table: `#`, `Disk`, `From`, `To`, plus a footer `Total: 15 moves (2⁴ − 1)`. |
| FR-8 | The app checks that Node.js and pnpm exist **before** rendering. If either is missing, it shows which one and points to the README; it does not crash. |
| FR-9 | During rendering, a spinner shows `Rendering video… 00:12`. |
| FR-10 | On success, the app shows the video's path (relative to the project root) and the render time. |
| FR-11 | After rendering, the after-render menu offers: same puzzle with new speed/quality, new puzzle, main menu, quit. |
| FR-12 | Ctrl+C at any point exits with `Goodbye!` and no traceback. If a render is running, it is stopped. |

### 4.2 Solver and engine

| ID | Requirement |
|---|---|
| FR-13 | `solve(n)` returns the full list of moves for n disks from A to C using B as helper. |
| FR-14 | The list length must equal 2ⁿ − 1. |
| FR-15 | `engine.apply(state, move)` refuses a move if: the source rod is empty, the moving disk is not on top of the source rod, or it would land on a smaller disk. It raises `IllegalMoveError`. |
| FR-16 | Before rendering, the app replays every move through the engine and confirms the final state has all disks on C, largest at the bottom. If this fails, it shows an internal error and does not render. |

### 4.3 Video

| ID | Requirement |
|---|---|
| FR-17 | Composition id `Hanoi`, size 1280×720, 30 fps. |
| FR-18 | Total length = `introFrames + totalMoves × framesPerMove + endPauseFrames + outroFrames`, set with Remotion's `calculateMetadata` from the props. |
| FR-19 | **Intro (introFrames):** title card `TOWER OF HANOI`, subtitle `<n> DISKS · <SPEED>`, then fades into the scene showing all disks on A. |
| FR-20 | **Moves:** each move takes `framesPerMove` frames, split into: **lift 30%** (disk rises straight up to a fixed height above the rod tops), **slide 40%** (moves horizontally to the target rod), **drop 30%** (falls to its resting spot on top of the target stack). Each part uses `Easing.inOut(Easing.cubic)`. |
| FR-21 | Disks not being moved stay still in their correct stacks. |
| FR-22 | **Move label** below the towers: `MOVE k / total · DISK d · X → Y`. Before the first move it shows `MOVE 0 / total`. After the last move it keeps showing the final move. |
| FR-23 | **End pause:** final state held still for `endPauseFrames`. |
| FR-24 | **Outro (outroFrames):** card `SOLVED!` + `<total> MOVES = 2^<n> − 1 ✓` (with a superscript exponent). |
| FR-25 | Visual style: dark background, amber CRT palette with one color per disk size (red, orange, yellow, green, blue — the same colors as the CLI moves table), rounded rods and pill-shaped disks like the reference image, labels A/B/C under each rod, pixel font Press Start 2P. |
| FR-26 | Disk widths scale with the disk count so 1 disk and 5 disks both look good. |

### 4.4 Output

| ID | Requirement |
|---|---|
| FR-27 | Video path: `videos/hanoi_<n>disks_<speed>_<sd|hd>.mp4`. The `videos/` folder is created if missing. |
| FR-28 | Rendering the same settings again overwrites the old file. |
| FR-29 | Codec: H.264 (Remotion default), MP4 container. |

---

## 5. Algorithms

### 5.1 Recursive solver

```
solve(n, source="A", helper="B", target="C"):
    if n == 0: return
    solve(n-1, source, target, helper)   # move n-1 disks out of the way
    record move: disk n, source → target # move the largest disk
    solve(n-1, helper, source, target)   # put n-1 disks back on top
```

- Moves: 2ⁿ − 1 → time O(2ⁿ)
- Recursion depth: n → space O(n) (not counting the stored move list)

### 5.2 Frame → disk position (Remotion `lib/timeline.ts`)

1. `f = frame − introFrames`. If `f < 0` → show starting state.
2. `k = floor(f / framesPerMove)` = index of the current move; `p = (f mod framesPerMove) / framesPerMove` = progress (0–1) inside that move.
3. If `k ≥ totalMoves` → show final state.
4. Get the state *before* move k by replaying moves 0…k−1 (pre-computed once with `useMemo`, so each frame is a quick lookup).
5. Draw every disk in its stack except the moving disk.
6. Moving disk position:
   - `p` in 0–0.3 → x = source rod x; y goes from its stack position up to `LIFT_Y`
   - `p` in 0.3–0.7 → y = `LIFT_Y`; x goes from source rod x to target rod x
   - `p` in 0.7–1.0 → x = target rod x; y goes from `LIFT_Y` down to the top of the target stack
7. Label shows move k+1.

### 5.3 Layout (at 1280×720)

| Item | Value |
|---|---|
| Rod x positions | A 320, B 640, C 960 |
| Base | full width minus margins, at y ≈ 560 |
| Rod height | enough to hold 5 disks with space above |
| `LIFT_Y` | above the rod tops |
| Disk height | ~34px, with small gaps |
| Disk width | from ~90px (smallest) to ~280px (largest), spread evenly over n |

Exact numbers are tuned in Phase 4 using Remotion Studio.

---

## 6. Render command

Run from `video/` as the working directory:

```
pnpm exec remotion render src/index.ts Hanoi <abs output path> --props=<abs path to .cache/props.json> --scale=<1|1.5>
```

- Python finds `pnpm` with `shutil.which("pnpm")` and runs it with `subprocess` using a **list of arguments** (no shell string). On Windows, `which` returns `pnpm.cmd`, which works this way.
- Output is captured. On failure, the last ~15 lines of the error output are shown in a red panel.

---

## 7. Error handling

| Situation | Behavior |
|---|---|
| Invalid menu/disk input | Red message + re-prompt |
| `node` not found | "Node.js is not installed. See README → Prerequisites." Return to menu. |
| `pnpm` not found | Same pattern for pnpm. |
| `video/node_modules` missing | "Remotion dependencies are not installed. Run `cd video && pnpm install`." |
| Render exits with error | Show error tail + "Render failed." Offer menu. |
| Engine finds an illegal move (bug) | "Internal error: illegal move #k." No render. |
| Ctrl+C | Stop any running render, print "Goodbye!", exit code 0. |
| Can't write to `videos/` | Show the OS error message, return to menu. |

---

## 8. Non-functional requirements

| ID | Requirement |
|---|---|
| NFR-1 | Runs on Windows 10+, macOS and Linux. |
| NFR-2 | Rendering works offline after setup (font bundled; no network calls). |
| NFR-3 | Animation is smooth: 30 fps, eased motion, no frame where a disk teleports. |
| NFR-4 | Target: a 5-disk, normal-speed, 720p render finishes in under ~2 minutes on a typical laptop (target, to be checked in Phase 5). |
| NFR-5 | Python code uses type hints; TypeScript in strict mode. |
| NFR-6 | Text is readable at 720p (font size ≥ 20px on the composition). |
| NFR-7 | Only one Python dependency (`rich`). |

---

## 9. Assumptions and constraints

- The user follows the README to install uv, Node.js LTS and pnpm.
- First render may take longer because Remotion downloads its headless browser.
- The disk limit (5) keeps video length and render time small.
- Remotion is used under its free license (individual developer).
