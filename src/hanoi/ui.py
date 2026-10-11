"""All Rich output: banner, menus, info screens, prompts, tables, spinner and errors.

app.py decides *what happens*; this file decides *how it looks*.
"""

from collections.abc import Iterator, Sequence
from contextlib import contextmanager

from rich import box
from rich.console import Console, Group, RenderableType
from rich.markup import escape
from rich.panel import Panel
from rich.progress import Progress, ProgressColumn, SpinnerColumn, Task, TextColumn
from rich.table import Table
from rich.text import Text

from hanoi import config, content
from hanoi.models import QUALITIES, SPEEDS, Move, Quality, RenderOptions, Speed

console = Console(highlight=False)

# ── Retro amber CRT palette ──
AMBER = "#ffb000"  # borders, menu numbers, prompt arrow
CREAM = "#ffe7a8"  # titles and headings
GREEN = "#3ddc84"  # success
RED = "#ff4d3d"  # errors
DISK_COLORS = ("#ff4d3d", "#ff9f1c", "#ffd23f", "#3ddc84", "#3fa7ff")  # disk 1 (smallest) → disk 5
BANNER_GRADIENT = ("#ffe08a", "#ffd04d", "#ffbf1f", "#ffaa00", "#ff9100", "#ff7a00")  # pale gold → orange, one per row

SPEED_NAMES: dict[Speed, str] = {"slow": "Slow", "normal": "Normal", "fast": "Fast"}
QUALITY_NAMES: dict[Quality, str] = {"low": "Low", "high": "High"}

_SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

# Block letters for the banner (6 rows each)
_GLYPHS: dict[str, tuple[str, ...]] = {
    "T": ("████████╗", "╚══██╔══╝", "   ██║   ", "   ██║   ", "   ██║   ", "   ╚═╝   "),
    "O": (" ██████╗ ", "██╔═══██╗", "██║   ██║", "██║   ██║", "╚██████╔╝", " ╚═════╝ "),
    "W": ("██╗    ██╗", "██║    ██║", "██║ █╗ ██║", "██║███╗██║", "╚███╔███╔╝", " ╚══╝╚══╝ "),
    "E": ("███████╗", "██╔════╝", "█████╗  ", "██╔══╝  ", "███████╗", "╚══════╝"),
    "R": ("██████╗ ", "██╔══██╗", "██████╔╝", "██╔══██╗", "██║  ██║", "╚═╝  ╚═╝"),
    "F": ("███████╗", "██╔════╝", "█████╗  ", "██╔══╝  ", "██║     ", "╚═╝     "),
    "H": ("██╗  ██╗", "██║  ██║", "███████║", "██╔══██║", "██║  ██║", "╚═╝  ╚═╝"),
    "A": (" █████╗ ", "██╔══██╗", "███████║", "██╔══██║", "██║  ██║", "╚═╝  ╚═╝"),
    "N": ("███╗   ██╗", "████╗  ██║", "██╔██╗ ██║", "██║╚██╗██║", "██║ ╚████║", "╚═╝  ╚═══╝"),
    "I": ("██╗", "██║", "██║", "██║", "██║", "╚═╝"),
    " ": ("  ",) * 6,
}


# ── Small helpers ──


def power_formula(disks: int) -> str:
    """'2⁴ − 1' for 4 disks."""
    return f"2{str(disks).translate(_SUPERSCRIPT)} − 1"


def _seconds_per_move(speed: Speed) -> str:
    return f"{config.FRAMES_PER_MOVE[speed] / config.FPS:g}s"


def _resolution(quality: Quality) -> str:
    scale = config.QUALITY_SCALE[quality]
    width = round(config.COMPOSITION_WIDTH * scale)
    height = round(config.COMPOSITION_HEIGHT * scale)
    return f"{height}p ({width}×{height})"


def _format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, secs = divmod(round(seconds), 60)
    return f"{minutes}m {secs:02d}s"


def _big_word(word: str) -> list[str]:
    glyphs = [_GLYPHS[letter] for letter in word]
    return ["".join(g[row].ljust(max(map(len, g))) for g in glyphs) for row in range(6)]


def _banner() -> RenderableType:
    top, bottom = _big_word("TOWER OF"), _big_word("HANOI")
    width = len(top[0])
    if console.width < width + 4:  # too narrow for the big letters
        return Text("  TOWER OF HANOI\n", style=f"bold {AMBER}")
    indent = (width - len(bottom[0])) // 2  # centre HANOI under TOWER OF
    banner = Text()
    for word, pad in ((top, 2), (bottom, 2 + indent)):
        for color, row in zip(BANNER_GRADIENT, word):
            banner.append(" " * pad + row + "\n", style=f"bold {color}")
    return banner


def _heading(text: str) -> Text:
    return Text(text, style=f"bold {CREAM}")


def _panel(body: RenderableType, title: str, border: str = AMBER) -> Panel:
    return Panel(
        body,
        title=f"[bold {CREAM}] {escape(title)} [/]",
        title_align="left",
        border_style=border,
        box=box.DOUBLE,
        padding=(0, 2),
        expand=False,
    )


def _numbered(items: Sequence[str]) -> Table:
    grid = Table.grid(padding=(0, 1))
    grid.add_column(style=f"bold {AMBER}")
    grid.add_column()
    for number, item in enumerate(items, start=1):
        grid.add_row(Text(f"{number}."), Text(item))
    return grid


def _menu(title: str, options: Sequence[tuple[str, str]], default: int | None = None) -> None:
    grid = Table.grid(padding=(0, 2))
    grid.add_column(style=f"bold {AMBER}")
    grid.add_column(style="bold")
    grid.add_column(style="dim")
    for number, (label, detail) in enumerate(options, start=1):
        if number == default:
            detail = f"{detail} · default" if detail else "default"
        grid.add_row(Text(f"[{number}]"), Text(label), Text(detail))
    console.print(_panel(grid, title))


def _screen(title: str) -> None:
    console.clear()
    console.print()
    console.rule(f"[bold {AMBER}]{escape(title)}[/]", style=CREAM)
    console.print()


# ── Prompts and messages ──


def ask(prompt: str) -> str:
    """Show a prompt and return what the user typed."""
    return console.input(f"[bold {AMBER}]▶[/] [bold]{escape(prompt)}[/] ")


def error(message: str) -> None:
    console.print(f"[bold {RED}]✗ {escape(message)}[/]")


def info(message: str) -> None:
    console.print(f"[dim]{escape(message)}[/]")


def wait_for_enter() -> None:
    console.input("\n[dim]Press Enter to return to the menu…[/]")


def error_panel(title: str, message: str, details: Sequence[str] = ()) -> None:
    parts: list[RenderableType] = [Text(message, style=f"bold {RED}")]
    if details:
        parts.append(Text("\n".join(details), style="dim"))
    console.print(_panel(Group(*parts), title, border=RED))


def goodbye() -> None:
    console.print(f"\n[bold {AMBER}]Goodbye![/]")


# ── Screens ──


def show_home() -> None:
    console.clear()
    console.print()
    console.print(_banner())
    console.print(
        f"  [bold {CREAM}]▸ RETRO PUZZLE SOLVER · {config.MIN_DISKS}–{config.MAX_DISKS} DISKS · MP4 VIDEO ◂[/]\n"
    )
    _menu(
        "MAIN MENU",
        [
            ("Solve a puzzle", "pick disks, speed and quality"),
            ("Rules", "how the puzzle works"),
            ("About the puzzle", "history, formula, recursion"),
            ("Quit", ""),
        ],
    )


def show_rules() -> None:
    _screen("RULES")
    body = Group(
        _heading("SETUP"),
        Text(content.RULES_SETUP),
        Text(),
        _heading("THE RULES"),
        _numbered(content.RULES),
        Text(),
        _heading("GOAL"),
        Text(content.RULES_GOAL),
    )
    console.print(_panel(body, "HOW TO PLAY"))


def show_about() -> None:
    _screen("ABOUT THE PUZZLE")
    disk_range = range(config.MIN_DISKS, config.MAX_DISKS + 1)
    counts = Table(box=box.ROUNDED, border_style="dim", show_header=False)
    counts.add_column(style=f"bold {CREAM}")
    for _ in disk_range:
        counts.add_column(justify="right")
    counts.add_row("Disks", *[str(n) for n in disk_range])
    counts.add_row("Moves", *[str(2**n - 1) for n in disk_range])

    complexity = Table.grid(padding=(0, 2))
    complexity.add_column(style=f"bold {AMBER}")
    complexity.add_column()
    for label, text in content.ABOUT_COMPLEXITY:
        complexity.add_row(Text(label), Text(text))

    body = Group(
        _heading("HISTORY"),
        Text(content.ABOUT_HISTORY),
        Text(),
        _heading("FEWEST MOVES"),
        Text(content.ABOUT_FORMULA),
        counts,
        Text(),
        _heading("RECURSION"),
        Text(content.ABOUT_RECURSION_INTRO),
        _numbered(content.ABOUT_RECURSION_STEPS),
        Text(content.ABOUT_RECURSION_OUTRO),
        Text(),
        _heading("COMPLEXITY"),
        complexity,
        Text(),
        Text(content.ABOUT_FUN_FACT, style="italic dim"),
    )
    console.print(_panel(body, "TOWER OF HANOI"))


def show_solve_header() -> None:
    _screen("SOLVE A PUZZLE")


def show_speed_menu() -> None:
    _menu(
        "SPEED",
        [(SPEED_NAMES[s], f"{_seconds_per_move(s)} per move") for s in SPEEDS],
        default=SPEEDS.index(config.DEFAULT_SPEED) + 1,
    )


def show_quality_menu() -> None:
    _menu(
        "QUALITY",
        [(QUALITY_NAMES[q], _resolution(q)) for q in QUALITIES],
        default=QUALITIES.index(config.DEFAULT_QUALITY) + 1,
    )


def show_summary(options: RenderOptions, min_moves: int, video_seconds: int) -> None:
    grid = Table.grid(padding=(0, 3))
    grid.add_column(style="dim")
    grid.add_column(style="bold")
    grid.add_row("Disks", str(options.disks))
    grid.add_row("Minimum moves", f"{min_moves}  ({power_formula(options.disks)})")
    grid.add_row("Speed", f"{SPEED_NAMES[options.speed]} · {_seconds_per_move(options.speed)} per move")
    grid.add_row("Quality", f"{QUALITY_NAMES[options.quality]} · {_resolution(options.quality)}")
    grid.add_row("Video length", f"~{video_seconds}s")
    console.print(_panel(grid, "READY TO RENDER", border=CREAM))


def show_moves(moves: Sequence[Move], disks: int) -> None:
    noun = "move" if len(moves) == 1 else "moves"
    table = Table(
        title="SOLUTION",
        title_style=f"bold {CREAM}",
        box=box.SIMPLE_HEAVY,
        header_style=f"bold {AMBER}",
        caption=f"Total: {len(moves)} {noun} ({power_formula(disks)})",
        caption_style=f"bold {GREEN}",
    )
    table.add_column("#", justify="right", style="dim")
    table.add_column("Disk")
    table.add_column("From", justify="center")
    table.add_column("To", justify="center")
    for move in moves:
        color = DISK_COLORS[(move.disk - 1) % len(DISK_COLORS)]
        table.add_row(
            str(move.number),
            Text(f"{move.disk} {'▰' * move.disk}", style=f"bold {color}"),
            move.source,
            move.target,
        )
    console.print(table)


class _ElapsedColumn(ProgressColumn):
    """Elapsed time as mm:ss."""

    def render(self, task: Task) -> Text:
        elapsed = int(task.elapsed or 0)
        return Text(f"{elapsed // 60:02d}:{elapsed % 60:02d}", style=CREAM)


@contextmanager
def rendering() -> Iterator[None]:
    """Spinner reading 'Rendering video… 00:12' while the block runs (FR-9)."""
    with Progress(
        SpinnerColumn(style=AMBER),
        TextColumn("[bold]Rendering video…"),
        _ElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("render", total=None)
        yield


def show_render_success(path: str, seconds: float) -> None:
    body = Group(
        Text.assemble(("✓ Video saved to: ", f"bold {GREEN}"), (path, "bold")),
        Text.assemble(("Render time: ", "dim"), _format_duration(seconds)),
    )
    console.print(_panel(body, "DONE", border=GREEN))


def show_after_render_menu() -> None:
    _menu(
        "WHAT NEXT?",
        [
            ("Same puzzle", "new speed / quality"),
            ("New puzzle", "pick a new number of disks"),
            ("Main menu", ""),
            ("Quit", ""),
        ],
    )
