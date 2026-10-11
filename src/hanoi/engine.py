"""Rule checker: replays moves on real rods, independently of the solver (FR-15, FR-16)."""

from hanoi.models import Move, Rod

# Each rod holds its disks from bottom to top, e.g. {"A": [3, 2, 1], "B": [], "C": []}
State = dict[Rod, list[int]]


class IllegalMoveError(Exception):
    """Raised when a move breaks one of the puzzle's rules."""

    def __init__(self, move: Move, reason: str) -> None:
        self.move = move
        self.reason = reason
        super().__init__(
            f"Illegal move #{move.number} (disk {move.disk}, {move.source} → {move.target}): {reason}"
        )


def initial_state(n: int) -> State:
    """All n disks on rod A, largest at the bottom."""
    return {"A": list(range(n, 0, -1)), "B": [], "C": []}


def apply(state: State, move: Move) -> State:
    """Return the new state after the move. The given state is not changed.

    Raises IllegalMoveError if the source rod is empty, the disk isn't on top
    of the source rod, or it would land on a smaller disk.
    """
    source = state[move.source]
    target = state[move.target]

    if not source:
        raise IllegalMoveError(move, f"rod {move.source} is empty")
    if source[-1] != move.disk:
        raise IllegalMoveError(move, f"disk {move.disk} is not on top of rod {move.source}")
    if target and target[-1] < move.disk:
        raise IllegalMoveError(move, f"disk {move.disk} can't go on smaller disk {target[-1]}")

    new_state: State = {rod: disks.copy() for rod, disks in state.items()}
    new_state[move.target].append(new_state[move.source].pop())
    return new_state


def verify_solution(n: int, moves: list[Move]) -> bool:
    """Replay every move from the start and check all n disks end on C, largest at the bottom.

    Raises IllegalMoveError (with the move number) as soon as a move breaks a rule.
    """
    state = initial_state(n)
    for move in moves:
        state = apply(state, move)
    return state == {"A": [], "B": [], "C": list(range(n, 0, -1))}
