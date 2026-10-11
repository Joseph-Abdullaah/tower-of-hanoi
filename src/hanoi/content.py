"""Text for the Rules and About screens, kept apart from the layout code in ui.py."""

# ── Rules screen ──
RULES_SETUP = (
    "There are three rods: A (source), B (helper) and C (destination). "
    "All the disks start on rod A, largest at the bottom, smallest at the top."
)
RULES = (
    "Move only one disk at a time.",
    "Only the top disk of a rod can be moved.",
    "A larger disk can never be placed on a smaller disk.",
)
RULES_GOAL = "Move the whole stack from rod A to rod C."

# ── About screen ──
ABOUT_HISTORY = "The Tower of Hanoi was invented by the French mathematician Édouard Lucas in 1883."
ABOUT_FORMULA = "The fewest moves needed for n disks is 2ⁿ − 1. Each extra disk doubles the moves, plus one."
ABOUT_RECURSION_INTRO = (
    "The puzzle is solved with recursion: a big problem made of smaller copies of itself. "
    "To move n disks from A to C:"
)
ABOUT_RECURSION_STEPS = (
    "Move the top n−1 disks from A to the helper rod B.",
    "Move the largest disk from A to C.",
    "Move the n−1 disks from B onto the largest disk on C.",
)
ABOUT_RECURSION_OUTRO = (
    "Moving n−1 disks is the same puzzle, only smaller, "
    "so the same three steps repeat until there are no disks left."
)
ABOUT_COMPLEXITY = (
    ("Time", "O(2ⁿ): the number of moves doubles with every extra disk."),
    ("Space", "O(n): the recursion only goes n calls deep."),
)
ABOUT_FUN_FACT = (
    "Legend says monks are moving a tower of 64 golden disks. "
    "At one move per second, they would need about 585 billion years."
)
