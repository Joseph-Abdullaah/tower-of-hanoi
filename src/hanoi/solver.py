"""Recursive Tower of Hanoi solver (SRS §5.1)."""

from hanoi.models import Move, Rod


def solve(n: int) -> list[Move]:
    """Return every move needed to shift n disks from A to C, using B as the helper.

    The list always has 2**n - 1 moves. Time O(2**n), recursion depth n.
    """
    if n < 0:
        raise ValueError(f"Number of disks can't be negative (got {n}).")

    moves: list[Move] = []

    def move_tower(count: int, source: Rod, helper: Rod, target: Rod) -> None:
        if count == 0:
            return
        move_tower(count - 1, source, target, helper)  # move n-1 disks out of the way
        moves.append(Move(number=len(moves) + 1, disk=count, source=source, target=target))  # move the largest disk
        move_tower(count - 1, helper, source, target)  # put n-1 disks back on top

    move_tower(n, "A", "B", "C")
    return moves
