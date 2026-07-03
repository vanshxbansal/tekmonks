"""Count rectangles on an N x N chessboard."""

from chessboard_squares import count_squares


def count_rectangles(board_size: int = 8, include_squares: bool = True) -> int:
    """
    Total rectangles = (sum of 1..n)^2 = (n(n+1)/2)^2

    Set include_squares=False to count only non-square rectangles.
    """
    if board_size < 1:
        raise ValueError("board_size must be at least 1")

    n = board_size
    total = (n * (n + 1) // 2) ** 2
    if include_squares:
        return total
    return total - count_squares(board_size)
