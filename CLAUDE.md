# CLAUDE.md — tower-of-hanoi

## What this project is
A retro-styled Python CLI that solves the Tower of Hanoi for 1–5 disks, prints every move, and renders a smooth MP4 video of the solution with Remotion. The app shows where the video was saved (it does not open it).

Full specs live in `/docs` — read them before coding:
- `docs/PRD.md` — what to build, features, user flow
- `docs/SRS.md` — how it behaves: data model, props contract, requirements (FR-x), algorithms, error handling
- `docs/TECH_STACK.md` — tools and why
- `docs/PROJECT_STRUCTURE.md` — folders and files
- `docs/PHASES.md` — build order and checklist (update checkboxes as phases finish)

## Stack (decided — don't change without asking)
- Python 3.11+, managed with **uv** (not pip). Only dependency: **rich**.
- Video: **Remotion 4.x** + React + TypeScript in `video/`, managed with **pnpm** (not npm/yarn).
- Python → Remotion via `.cache/props.json` + `pnpm exec remotion render src/index.ts Hanoi … --props=… --scale=1|1.5`.

## Key decisions
- Rods: A (source), B (helper), C (destination). Disks: 1 = smallest.
- Disks 1–5 only. Speeds: slow 1.5s / normal 0.8s / fast 0.4s per move (45/24/12 frames at 30 fps).
- Quality: low 720p (scale 1) / high 1080p (scale 1.5). Composition is 1280×720.
- Each move animates lift (30%) → slide (40%) → drop (30%) with ease-in-out. No jumping.
- Move label: `MOVE 5 / 15 · DISK 1 · A → C`. Intro title card + outro `SOLVED! 15 MOVES = 2⁴ − 1 ✓`.
- Retro style: dark background, amber CRT palette (amber `#ffb000` UI, cream `#ffe7a8` text; disks 1→5 red `#ff4d3d`, orange `#ff9f1c`, yellow `#ffd23f`, green `#3ddc84`, blue `#3fa7ff`; no pink/purple), Press Start 2P font bundled in `video/public/fonts` (offline).
- All timing/limit numbers live in `src/hanoi/config.py`; Python sends them in props. Remotion never hard-codes them.
- Output: `videos/hanoi_<n>disks_<speed>_<sd|hd>.mp4`.
- No tests/CI, no play mode, no auto-opening the video (future ideas only).
- Users set up by reading the README; the app does not auto-install anything.

## Commands
- `uv sync` · `uv run hanoi`
- `cd video && pnpm install` · `pnpm studio` · `pnpm render`

## Working with Joseph
- He's a computing/IT student and app developer; explain in plain English, not heavy technical prose.
- Build phase by phase (see PHASES.md). Finish and confirm one phase before starting the next.
- Use type hints in Python and strict TypeScript.
