"""Framework-independent Peg Solitaire model for CS 449 Sprint 2.

Supported configurations are conventional examples, not a course-defined size
range: English, Hexagon, and Diamond each at sizes 7 and 9.
Board size means maximum displayed span; these sizes are assumptions.
"""

from __future__ import annotations


Position = tuple[int, int]
Move = tuple[Position, Position]


class SolitaireGame:
    """Store the board, enforce legal jumps, and report terminal states."""

    # Geometry-specific axial directions for a triangular/hexagonal lattice.
    ORTHOGONAL: tuple[Position, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))
    HEXAGONAL: tuple[Position, ...] = (
        (1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)
    )
    SUPPORTED_SIZES = {"English": (7, 9), "Hexagon": (7, 9), "Diamond": (7, 9)}

    def __init__(self, board_type: str = "English", size: int = 7) -> None:
        self.board_type = ""
        self.size = 0
        self.positions: frozenset[Position] = frozenset()
        self.pegs: set[Position] = set()
        self.new_game(board_type, size)

    @classmethod
    def valid_configuration(cls, board_type: str, size: int) -> bool:
        """Check the explicitly supported combinations without coercing input."""
        return (
            isinstance(board_type, str)
            and type(size) is int
            and size in cls.SUPPORTED_SIZES.get(board_type, ())
        )

    @classmethod
    def board_types(cls) -> tuple[str, ...]:
        return tuple(cls.SUPPORTED_SIZES)

    @classmethod
    def sizes_for(cls, board_type: str) -> tuple[int, ...]:
        return cls.SUPPORTED_SIZES.get(board_type, ())

    @staticmethod
    def _positions_for(board_type: str, size: int) -> frozenset[Position]:
        radius = size // 2
        if board_type == "English":
            # A generalized cross with central band of width 3.
            return frozenset(
                (row, col)
                for row in range(size)
                for col in range(size)
                if radius - 1 <= row <= radius + 1
                or radius - 1 <= col <= radius + 1
            )
        if board_type == "Diamond":
            return frozenset(
                (row, col)
                for row in range(size)
                for col in range(size)
                if abs(row - radius) + abs(col - radius) <= radius
            )
        # Axial hexagonal coordinates: center (0,0), side length 4.
        return frozenset(
            (q, r)
            for q in range(-radius, radius + 1)
            for r in range(-radius, radius + 1)
            if max(abs(q), abs(r), abs(q + r)) <= radius
        )

    def new_game(self, board_type: str | None = None, size: int | None = None) -> None:
        """Initialize the selected configuration with the central cell empty.

        No state is changed if a proposed configuration is invalid.
        """
        selected_type = self.board_type if board_type is None else board_type
        selected_size = self.size if size is None else size
        if not self.valid_configuration(selected_type, selected_size):
            raise ValueError(f"Unsupported board configuration: {selected_type!r}, {selected_size!r}")
        positions = self._positions_for(selected_type, selected_size)
        center = (0, 0) if selected_type == "Hexagon" else (selected_size // 2,) * 2
        if center not in positions:
            raise ValueError("Board has no valid central hole")
        self.board_type = selected_type
        self.size = selected_size
        self.positions = positions
        self.pegs = set(positions - {center})

    @property
    def directions(self) -> tuple[Position, ...]:
        return self.HEXAGONAL if self.board_type == "Hexagon" else self.ORTHOGONAL

    def is_valid_move(self, source: Position, destination: Position) -> bool:
        """Require occupied source/jumped hole and playable empty destination."""
        if source not in self.pegs or destination not in self.positions or destination in self.pegs:
            return False
        delta = (destination[0] - source[0], destination[1] - source[1])
        if not any(delta == (2 * dx, 2 * dy) for dx, dy in self.directions):
            return False
        jumped = (source[0] + delta[0] // 2, source[1] + delta[1] // 2)
        return jumped in self.pegs

    def make_move(self, source: Position, destination: Position) -> bool:
        """Apply one jump, or leave the board untouched when illegal."""
        if not self.is_valid_move(source, destination):
            return False
        jumped = ((source[0] + destination[0]) // 2,
                  (source[1] + destination[1]) // 2)
        self.pegs.remove(source)
        self.pegs.remove(jumped)
        self.pegs.add(destination)
        return True

    def legal_moves(self) -> list[Move]:
        """Return all legal jumps from the current position."""
        moves: list[Move] = []
        for source in sorted(self.pegs):
            for dx, dy in self.directions:
                destination = (source[0] + 2 * dx, source[1] + 2 * dy)
                if self.is_valid_move(source, destination):
                    moves.append((source, destination))
        return moves

    def is_game_over(self) -> bool:
        return not self.legal_moves()

    def remaining_pegs(self) -> int:
        return len(self.pegs)
