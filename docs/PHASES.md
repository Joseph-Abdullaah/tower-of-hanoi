# Build Phases — tower-of-hanoi

Small project, so no design system or screen designs. Six phases, each ending with something you can run or see.

---

## Phase 1 — Docs ✅
**Goal:** agree on what we're building.

- [x] TECH_STACK.md
- [x] PRD.md
- [x] SRS.md
- [x] PROJECT_STRUCTURE.md
- [x] PHASES.md

**Done when:** docs are in `/docs` and committed.

---

## Phase 2 — Project setup + core logic (Python) ✅
**Goal:** the puzzle is solved correctly, with no UI yet.

- [x] Create the repo, `.gitignore`, `.python-version`
- [x] `uv init` → set up `pyproject.toml` with `rich` and the `hanoi` command
- [x] `config.py` — all constants
- [x] `models.py` — `Move`, `RenderOptions`, `Rod`
- [x] `solver.py` — recursive `solve(n)`
- [x] `engine.py` — rod state, `apply()`, `IllegalMoveError`, `verify_solution()`
- [x] Quick check: for n = 1…5, move count = 2ⁿ − 1 and `verify_solution()` passes

**Done when:** `uv run python -c "…"` prints correct moves for 3 disks (7 moves) and verification passes for 1–5.

---

## Phase 3 — Retro CLI (Python + Rich) ✅
**Goal:** the full menu experience works, with rendering faked.

- [x] `content.py` — rules + about text
- [x] `ui.py` — banner, main menu, rules, about, disk/speed/quality prompts, summary panel, moves table, error panel
- [x] `app.py` — main loop, routing, input validation, after-render menu, Ctrl+C handling
- [x] Temporarily fake the render step (e.g. 2-second spinner, then a fake path)

**Done when:** `uv run hanoi` lets you go through every screen, bad input never crashes it, and the moves table is correct.

---

## Phase 4 — Remotion video ✅
**Goal:** a beautiful, smooth video using default test props.

- [x] `pnpm create video` (blank TypeScript template) inside `video/`, then clean it up
- [x] Add Press Start 2P font to `public/fonts` + load it in `theme.ts`
- [x] `types.ts` — props type matching SRS §3.3
- [x] `Root.tsx` — `Hanoi` composition, 1280×720, 30 fps, `calculateMetadata`, default props (3 disks)
- [x] `layout.ts` + `theme.ts` — positions, sizes, colors
- [x] `Base`, `Rod`, `Disk` — static scene matching the reference image
- [x] `timeline.ts` — frame → state + lift/slide/drop with easing
- [x] `MoveLabel`, `IntroCard`, `OutroCard`
- [x] Tune it in `pnpm studio` with 1, 3 and 5 disks and all three speeds
- [x] `pnpm render` → test MP4

**Done when:** the test video plays smoothly, the counter is right, and nothing jumps.

---

## Phase 5 — Connect Python ↔ Remotion ✅
**Goal:** the real end-to-end flow.

- [x] `renderer.py` — `check_requirements()` (node, pnpm, `video/node_modules`)
- [x] `build_props()` + `write_props()` → `.cache/props.json`
- [x] `render()` — run `pnpm exec remotion render …` with `--props` and `--scale`, capture output, measure time
- [x] Replace the fake render in `app.py`
- [x] Error paths: missing tools, render failure, Ctrl+C during render
- [x] Check NFR-4: time a 5-disk normal 720p render

**Done when:** from `uv run hanoi`, choosing 4 disks / normal / high produces `videos/hanoi_4disks_normal_hd.mp4` and shows its path.

---

## Phase 6 — README + polish
**Goal:** anyone can clone and run it.

- [x] README: description, preview GIF/screenshot, prerequisites (uv, Node LTS, pnpm), install, run, how it works, troubleshooting (incl. Linux libraries), Remotion license line, future ideas
- [ ] Fresh-clone test on at least one other OS or machine *(passed on Windows 11, same machine; another OS still to do)*
- [x] Final visual polish (colors, timing, label spacing)
- [ ] Tag `v0.1.0`

**Done when:** a fresh clone → README steps → finished video works with no extra help.
