# Tech Stack — tower-of-hanoi

## 1. Overview

The project has **two parts**, written in two languages:

| Part | Language | Job |
|---|---|---|
| **CLI app** | Python | Retro menu, rules, user input, solving the puzzle, printing the move list, starting the video render, showing where the video was saved |
| **Video renderer** | TypeScript + React (Remotion) | Drawing the base, rods and disks, animating every move smoothly, and writing the final MP4 file |

Python is the "brain" and the "front desk". Remotion is the "animation studio". They talk through **one JSON file** (`props.json`).

---

## 2. Python side (CLI)

| Tool | Role | Why this choice |
|---|---|---|
| **Python 3.11+** | Language | Modern, stable, good typing support. `uv` can install it automatically. |
| **uv** | Package + project manager | One tool for installing Python, creating the virtual environment and installing dependencies. Fast, and `uv sync` + `uv run hanoi` is all a user needs. |
| **Rich** | Terminal UI | Colors, panels, tables, ASCII banners, styled prompts and a spinner while the video renders. Works on Windows, macOS and Linux. |
| **hatchling** | Build backend | Small, standard backend so `pyproject.toml` can define the `hanoi` command (`uv run hanoi`). |
| Standard library: `subprocess`, `json`, `pathlib`, `shutil`, `dataclasses`, `time` | Glue | Run the Remotion render, write props, build paths, find `pnpm`, hold move data, time the render. No extra packages needed. |

**Only one third-party Python dependency: `rich`.**

---

## 3. Video side (Remotion)

| Tool | Role | Why this choice |
|---|---|---|
| **Node.js (current LTS)** | JavaScript runtime | Required by Remotion. |
| **pnpm** | Node package manager | Fast installs, small disk usage, strict lockfile (`pnpm-lock.yaml`). |
| **Remotion 4.x** | Video engine | Write the animation as React components; Remotion renders each frame and encodes the MP4. FFmpeg and a headless browser come with it — no system FFmpeg needed. |
| **React** | UI library for the scenes | Each visual piece (rod, disk, label) is a component. |
| **TypeScript** | Language | Type-safe props contract (moves, disk count, speed). Catches mistakes before rendering. |
| **Remotion `interpolate()` + `Easing`** | Motion | Smooth lift → slide → drop movement with ease-in-out curves. No jumps. |
| **Press Start 2P** (font file, bundled in `video/public/fonts`) | Retro pixel font | Arcade look. Bundled locally so rendering works **offline**. Licensed under SIL Open Font License. |
| **Remotion Studio** (`pnpm exec remotion studio`) | Dev preview | Preview the animation in the browser while building, without rendering the full video each time. |

### Remotion license note
Remotion is **source-available**, not open source. It is **free** for individuals (personal or commercial use) and teams of up to 3 people. This project qualifies. The README will include one line about this.

---

## 4. How the two parts connect

```
Python CLI ──writes──▶ .cache/props.json
     │
     └──runs──▶ pnpm exec remotion render src/index.ts Hanoi <output.mp4>
                   --props=<path to props.json> --scale=<1 or 1.5>
                   (working directory: video/)
                                   │
                                   ▼
                          videos/hanoi_4disks_normal_hd.mp4
```

- Props go through a **file**, not inline JSON, because Windows shells strip the quote characters from inline JSON.
- **Quality** uses Remotion's `--scale` flag on a 1280×720 composition:
  - Low → scale `1` → **1280×720 (720p)**
  - High → scale `1.5` → **1920×1080 (1080p)**

---

## 5. User prerequisites (what someone cloning the repo needs)

| Requirement | How to get it |
|---|---|
| Git | git-scm.com |
| uv | docs.astral.sh/uv (installs Python for you) |
| Node.js LTS | nodejs.org |
| pnpm | pnpm.io/installation |

Setup is two commands (full steps in the README):

```bash
uv sync                     # Python side
cd video && pnpm install    # Remotion side (downloads its headless browser on first render)
```

Run:

```bash
uv run hanoi
```

> **Linux note:** Remotion's headless browser may need a few system libraries on minimal Linux installs. The README will list the install command from Remotion's Linux docs.

---

## 6. What we are deliberately NOT using

| Not using | Reason |
|---|---|
| Manim | Heavy system setup (FFmpeg, Cairo/Pango on Linux, optional LaTeX). Remotion is easier to install and fits your React skills. |
| Terminal animation (curses, ANSI) | The animation must be a real video. |
| Textual / Typer / Click | Rich alone covers the menu and prompts; the app has no command-line flags. |
| pytest / CI | Not required for this project. The engine still checks every move against the rules at runtime. |
| Google Fonts loader | Would need internet during render. A bundled font file works offline. |
