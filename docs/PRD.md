# Product Requirements Document (PRD) — tower-of-hanoi

**Owner:** Joseph
**Type:** Python CLI app + Remotion video renderer
**Status:** Planning
**Last updated:** 2026-10-11

---

## 1. Summary

`tower-of-hanoi` is a retro-styled command-line app. The user picks how many disks to use (1–5), a video speed and a video quality. The app solves the Tower of Hanoi puzzle, prints every move in the terminal, and renders a **smooth animated MP4 video** of the solution with a live move counter. When the render finishes, the app shows where the video was saved.

---

## 2. Background

The Tower of Hanoi was invented by French mathematician Édouard Lucas in 1883.

**Setup:** three rods — **A** (source), **B** (helper), **C** (destination) — and *n* disks of different sizes stacked on rod A, largest at the bottom.

**Rules:**
1. Move only one disk at a time.
2. Only the top disk of a rod can be moved.
3. A larger disk can never be placed on a smaller disk.

**Goal:** move the whole stack from rod A to rod C.

**Key facts the app teaches:**
- Minimum moves = **2ⁿ − 1** (3 disks → 7, 4 → 15, 5 → 31).
- Solved with **recursion**: move n−1 disks to the helper rod, move the largest disk to the destination, then move the n−1 disks on top of it.
- Time complexity **O(2ⁿ)**, space complexity **O(n)**.

---

## 3. Goals

| # | Goal |
|---|---|
| G1 | Solve the puzzle for 1–5 disks in the minimum number of moves. |
| G2 | Produce a clear, smooth, good-looking video of the solution (no jumping or GIF-style frames). |
| G3 | Show the move count live in the video and the full move list in the terminal. |
| G4 | Give the CLI a fun retro arcade feel with a structured menu and rules screen. |
| G5 | Anyone can clone the repo, install dependencies and run it by following the README. |

## 4. Non-goals (out of scope for now)

- **Play mode** (user moves disks themselves) — possible future feature.
- More than 5 disks.
- Animation inside the terminal.
- Opening the video automatically.
- Changing video speed during playback (speed is chosen before rendering).
- Automated tests / CI.
- Publishing to PyPI or npm.

---

## 5. Target users

- **Students** learning recursion and algorithms who want to *see* how the solution works.
- **Viewers of Joseph's GitHub/portfolio** who clone the repo and try it.
- **Joseph** himself, as a learning project combining Python and React video rendering.

---

## 6. User flow

```
Start app (uv run hanoi)
   │
   ▼
Retro title banner
   │
   ▼
MAIN MENU
 [1] Solve a puzzle
 [2] Rules
 [3] About the puzzle (history, formula, recursion)
 [4] Quit
   │
   ├─[2]/[3]──▶ Info screen ──▶ "Press Enter to return" ──▶ MAIN MENU
   │
   └─[1]──▶ Number of disks (1–5)
              ▼
            Speed: Slow / Normal / Fast
              ▼
            Quality: Low (720p) / High (1080p)
              ▼
            Summary panel (disks, min moves, speed, quality, estimated video length)
            Confirm? [Y/n]
              ▼
            Solve ──▶ Move list table in terminal
              ▼
            Rendering… (spinner + elapsed time)
              ▼
            "✓ Video saved to: videos/hanoi_4disks_normal_hd.mp4"
              ▼
            AFTER-RENDER MENU
             [1] Same puzzle, different speed/quality
             [2] New puzzle
             [3] Main menu
             [4] Quit
```

---

## 7. Features

### 7.1 CLI (Python + Rich)

| ID | Feature | Priority |
|---|---|---|
| C1 | Retro ASCII title banner with amber CRT colors | Must |
| C2 | Numbered main menu (Solve, Rules, About, Quit) | Must |
| C3 | Rules screen (setup, 3 rules, goal) | Must |
| C4 | About screen (Lucas 1883, 2ⁿ − 1, recursion, complexity) | Must |
| C5 | Disk input 1–5 with validation and friendly re-prompt | Must |
| C6 | Speed choice: Slow / Normal / Fast | Must |
| C7 | Quality choice: Low 720p / High 1080p | Must |
| C8 | Summary panel before rendering, with confirm | Should |
| C9 | Move list printed as a styled table (Move #, Disk, From, To) | Must |
| C10 | Spinner with elapsed time during rendering | Must |
| C11 | Show saved video path and total render time | Must |
| C12 | After-render menu (re-render, new puzzle, main menu, quit) | Should |
| C13 | Clear error messages if Node/pnpm is missing or the render fails | Must |
| C14 | Clean exit on Ctrl+C (no ugly traceback) | Must |

### 7.2 Video (Remotion)

| ID | Feature | Priority |
|---|---|---|
| V1 | Scene like the reference image: base platform, three rounded rods, pill-shaped disks of decreasing width | Must |
| V2 | Rod labels **A**, **B**, **C** | Must |
| V3 | Smooth 3-step motion per move: **lift** up the rod → **slide** across → **drop** down, with easing | Must |
| V4 | Move label under the towers, e.g. `MOVE 5 / 15 · DISK 1 · A → C` (includes the move counter) | Must |
| V5 | Intro title card: `TOWER OF HANOI` + disk count + speed | Should |
| V6 | Outro summary card: `SOLVED! 15 MOVES = 2⁴ − 1 ✓` | Should |
| V7 | Retro styling: dark background, amber CRT palette (same disk colors as the CLI), pixel font (Press Start 2P) | Must |
| V8 | Speed controls time per move: Slow 1.5s, Normal 0.8s, Fast 0.4s | Must |
| V9 | Quality: 720p (low) or 1080p (high) | Must |
| V10 | Video length adapts automatically to the number of moves | Must |

### 7.3 Project / repo

| ID | Feature | Priority |
|---|---|---|
| R1 | README with prerequisites, install steps (uv + pnpm), run command, troubleshooting | Must |
| R2 | Output videos saved in `videos/`, ignored by git | Must |
| R3 | Clear file names: `hanoi_<n>disks_<speed>_<quality>.mp4` | Must |

---

## 8. Example video lengths

Approximate, including ~2s intro, ~1s pause and ~3s outro.

| Disks | Moves | Slow (1.5s) | Normal (0.8s) | Fast (0.4s) |
|---|---|---|---|---|
| 1 | 1 | ~8s | ~7s | ~6s |
| 3 | 7 | ~17s | ~12s | ~9s |
| 4 | 15 | ~29s | ~18s | ~12s |
| 5 | 31 | ~53s | ~31s | ~18s |

---

## 9. Success criteria

1. For every n from 1 to 5, the app makes exactly 2ⁿ − 1 moves and never breaks a rule.
2. The video shows every move smoothly, the counter matches the terminal move list, and the final frame shows all disks on rod C.
3. A new user on Windows, macOS or Linux can go from `git clone` to a finished video by following only the README.
4. Wrong input never crashes the app.

---

## 10. Future ideas (not now)

- Play mode: user makes moves, app checks the rules.
- Step-by-step terminal mode (press Enter for each move).
- Show the recursion tree beside the towers in the video.
- Custom source/destination rods.
- Background music / move sound effects.
