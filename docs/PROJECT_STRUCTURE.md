# Project Structure — tower-of-hanoi

```
tower-of-hanoi/
├── README.md                  # What it is, prerequisites, install, run, troubleshooting, license note
├── LICENSE
├── .gitignore                 # .venv/, .cache/, videos/*.mp4, video/node_modules/, video/out/, __pycache__/
├── .python-version            # e.g. 3.12 — uv uses this
├── pyproject.toml             # Project metadata, rich dependency, `hanoi` command
├── uv.lock                    # Exact Python dependency versions (committed)
│
├── docs/
│   ├── TECH_STACK.md
│   ├── PRD.md
│   ├── SRS.md
│   ├── PROJECT_STRUCTURE.md
│   └── PHASES.md
│
├── src/
│   └── hanoi/                 # ── PYTHON CLI ──
│       ├── __init__.py
│       ├── __main__.py        # Allows `python -m hanoi`; calls app.main()
│       ├── app.py             # main(): main loop, menu routing, solve→render flow, Ctrl+C handling
│       ├── ui.py              # All Rich output: banner, menus, rules, about, prompts, tables, spinner, errors
│       ├── content.py         # Text for the rules and about screens (kept apart from layout code)
│       ├── config.py          # Constants: disk limits, FPS, frames per speed, quality scales, paths
│       ├── models.py          # Move, RenderOptions dataclasses; Rod type
│       ├── solver.py          # solve(n) -> list[Move] (recursive)
│       ├── engine.py          # Rod state, apply(), IllegalMoveError, verify_solution()
│       └── renderer.py        # check_requirements(), build_props(), write_props(), render() via pnpm
│
├── video/                     # ── REMOTION PROJECT ──
│   ├── package.json           # remotion, @remotion/cli, react, react-dom, typescript
│   ├── pnpm-lock.yaml         # Exact Node dependency versions (committed)
│   ├── tsconfig.json          # strict mode
│   ├── remotion.config.ts     # Remotion settings (e.g. image format, overwrite)
│   ├── public/
│   │   └── fonts/
│   │       ├── PressStart2P-Regular.ttf
│   │       └── OFL.txt        # Font license
│   └── src/
│       ├── index.ts           # registerRoot(Root)
│       ├── Root.tsx           # <Composition id="Hanoi" …> + calculateMetadata + default props for Studio
│       ├── HanoiVideo.tsx     # Puts the parts in order: Intro → Scene → Outro
│       ├── types.ts           # Rod, Move, HanoiProps (matches props.json)
│       ├── components/
│       │   ├── Scene.tsx      # Base + 3 rods + all disks + move label for the current frame
│       │   ├── Base.tsx       # Platform
│       │   ├── Rod.tsx        # One rounded rod + its A/B/C label
│       │   ├── Disk.tsx       # One pill-shaped disk at an (x, y) position
│       │   ├── MoveLabel.tsx  # "MOVE 5 / 15 · DISK 1 · A → C"
│       │   ├── IntroCard.tsx  # Title card
│       │   └── OutroCard.tsx  # "SOLVED! 15 MOVES = 2⁴ − 1 ✓"
│       └── lib/
│           ├── theme.ts       # Colors, amber CRT disk palette, font loading, sizes
│           ├── layout.ts      # Rod x positions, base y, lift height, disk width/height math
│           └── timeline.ts    # Frame → states, moving disk position (lift/slide/drop + easing)
│
├── .cache/                    # Created at runtime; holds props.json (git-ignored)
└── videos/                    # Rendered MP4s land here (git-ignored, keep .gitkeep)
    └── .gitkeep
```

---

## Why it's split this way

| Decision | Reason |
|---|---|
| `src/hanoi/` (src layout) | Standard Python layout; lets `uv run hanoi` work as a real command. |
| `ui.py` separate from `app.py` | `app.py` decides *what happens*; `ui.py` decides *how it looks*. Changing the retro style never touches the flow logic. |
| `solver.py` separate from `engine.py` | The solver creates moves; the engine independently checks them. If the solver has a bug, the engine catches it before rendering. |
| `renderer.py` is the only file that knows about Node/pnpm | If we ever change the video tool again, only this file changes. |
| `config.py` holds all numbers | One place to change speeds, limits or quality. Python passes frame numbers to Remotion in the props, so values never get out of sync. |
| `video/` is its own Node project | Keeps `package.json` and `node_modules` away from the Python files. |
| `lib/timeline.ts` separate from components | All the "where is each disk at this frame" math lives in one place, so components only draw. |

---

## Key files at a glance

### `pyproject.toml` (shape)

```toml
[project]
name = "tower-of-hanoi"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["rich"]

[project.scripts]
hanoi = "hanoi.app:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### `video/package.json` scripts (shape)

```json
{
  "scripts": {
    "studio": "remotion studio src/index.ts",
    "render": "remotion render src/index.ts Hanoi out/test.mp4"
  }
}
```

- `pnpm studio` → preview while building (Phase 4)
- `pnpm render` → manual test render with default props

---

## Commands summary

| Task | Command |
|---|---|
| Install Python deps | `uv sync` |
| Install Remotion deps | `cd video && pnpm install` |
| Run the app | `uv run hanoi` |
| Preview video while developing | `cd video && pnpm studio` |
