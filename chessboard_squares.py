"""Count squares on an N x N chessboard (all sizes)."""


def count_squares(board_size: int = 8) -> int:
    """
    Total squares = 1^2 + 2^2 + ... + n^2 = n(n+1)(2n+1) / 6
    """
    if board_size < 1:
        raise ValueError("board_size must be at least 1")

    n = board_size
    return n * (n + 1) * (2 * n + 1) // 6


def count_visible_unit_squares(board_size: int = 8) -> int:
    """Number of 1x1 squares on the board."""
    return board_size * board_size
