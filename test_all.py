"""Run sample test cases for all puzzles and algorithms."""

from lemon_watchman import initial_lemons
from chessboard_squares import count_squares, count_visible_unit_squares
from chessboard_rectangles import count_rectangles
from shortest_path import (
    bfs_shortest_path,
    dijkstra_shortest_path,
    bellman_ford_shortest_path,
    floyd_warshall_all_pairs,
)


def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def test_lemon_watchman() -> None:
    print_header("1. Lemon / Watchman / Farm Puzzle")
    for n in [1, 2, 3, 4, 5]:
        result = initial_lemons(n)
        print(f"  N = {n} gates -> initially stole {result} lemons")


def test_chessboard_squares() -> None:
    print_header("2. Number of Squares on a Chessboard (8x8)")
    n = 8
    unit = count_visible_unit_squares(n)
    total = count_squares(n)
    print(f"  Visible 1x1 squares: {unit}")
    print(f"  Total squares (all sizes): {total}")


def test_chessboard_rectangles() -> None:
    print_header("3. Number of Rectangles on a Chessboard (8x8)")
    n = 8
    all_rects = count_rectangles(n, include_squares=True)
    non_square_rects = count_rectangles(n, include_squares=False)
    print(f"  Total rectangles (including squares): {all_rects}")
    print(f"  Rectangles excluding squares: {non_square_rects}")
    print(f"  Check: {all_rects} - {count_squares(n)} = {non_square_rects}")


def test_shortest_paths() -> None:
    print_header("4. Shortest Path Between Two Nodes")

    # Unweighted -> BFS
    unweighted = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    dist, path = bfs_shortest_path(unweighted, "A", "D")
    print(f"  BFS (unweighted): A -> D")
    print(f"    Distance (hops): {int(dist)}")
    print(f"    Path: {' -> '.join(path)}")

    # Weighted positive -> Dijkstra
    weighted = {
        "A": [("B", 4.0), ("C", 2.0)],
        "B": [("D", 5.0)],
        "C": [("B", 1.0), ("D", 8.0)],
        "D": [],
    }
    dist, path = dijkstra_shortest_path(weighted, "A", "D")
    print(f"\n  Dijkstra (non-negative weights): A -> D")
    print(f"    Distance: {dist}")
    print(f"    Path: {' -> '.join(path)}")

    # Negative weights -> Bellman-Ford
    with_negative = {
        "A": [("B", 1.0), ("C", 4.0)],
        "B": [("C", -2.0), ("D", 3.0)],
        "C": [("D", 1.0)],
        "D": [],
    }
    dist, path = bellman_ford_shortest_path(with_negative, "A", "D")
    print(f"\n  Bellman-Ford (negative weights allowed): A -> D")
    print(f"    Distance: {dist}")
    print(f"    Path: {' -> '.join(path)}")

    # All pairs -> Floyd-Warshall
    inf = float("inf")
    labels = ["A", "B", "C", "D"]
    matrix = [
        [0, 3, inf, 7],
        [8, 0, 2, inf],
        [5, inf, 0, 1],
        [2, inf, inf, 0],
    ]
    dist_matrix, paths = floyd_warshall_all_pairs(matrix, labels)
    print(f"\n  Floyd-Warshall (all-pairs): A -> D")
    print(f"    Distance: {dist_matrix[0][3]}")
    print(f"    Path: {' -> '.join(paths[('A', 'D')])}")


def main() -> None:
    print("Running all puzzle and algorithm test cases...\n")
    test_lemon_watchman()
    test_chessboard_squares()
    test_chessboard_rectangles()
    test_shortest_paths()
    print("\n" + "=" * 60)
    print("All tests completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
