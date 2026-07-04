"""Run sample test cases for all puzzles and algorithms."""

import sys
from io import StringIO

from lemon_watchman import initial_lemons
from chessboard_squares import count_squares, count_visible_unit_squares
from chessboard_rectangles import count_rectangles
from shortest_path import (
    bfs_shortest_path,
    dijkstra_shortest_path,
    bellman_ford_shortest_path,
    floyd_warshall_all_pairs,
)

WIDTH = 72


def rule(char: str = "─") -> None:
    print(char * WIDTH)


def section(num: int, title: str) -> None:
    print()
    rule("═")
    print(f"  {num}. {title}")
    rule("═")


def label(text: str) -> None:
    print(f"  {text}")


def result(key: str, value: str) -> None:
    print(f"    {key:<22} {value}")


def blank() -> None:
    print()


def test_lemon_watchman() -> None:
    section(1, "Lemon / Watchman / Farm Puzzle")
    label("Problem : At each of N gates, a watchman takes half the lemons")
    label("          plus one more. After all gates, 1 lemon remains.")
    label("Approach: Work backwards — before a gate: 2 × (remaining + 1)")
    blank()
    label("Gate Count (N)    Initial Lemons Stolen")
    rule()
    for n in [1, 2, 3, 4, 5]:
        lemons = initial_lemons(n)
        print(f"       {n}                  {lemons}")
    blank()
    n_demo = 3
    result("Example (N=3)", f"{initial_lemons(n_demo)} lemons → 1 remains after 3 gates")


def test_chessboard_squares() -> None:
    section(2, "Number of Squares on a Chessboard")
    n = 8
    unit = count_visible_unit_squares(n)
    total = count_squares(n)
    label(f"Board   : {n} × {n} standard chessboard")
    label("Formula : 1² + 2² + … + n² = n(n+1)(2n+1) / 6")
    blank()
    result("1×1 squares (visible)", str(unit))
    result("All sizes combined", str(total))
    blank()
    label("Breakdown by size:")
    for size in range(1, n + 1):
        count = (n - size + 1) ** 2
        print(f"      {size}×{size} squares : {count:>3}")


def test_chessboard_rectangles() -> None:
    section(3, "Number of Rectangles on a Chessboard")
    n = 8
    squares = count_squares(n)
    all_rects = count_rectangles(n, include_squares=True)
    non_square_rects = count_rectangles(n, include_squares=False)
    label(f"Board   : {n} × {n} standard chessboard")
    label("Formula : (1 + 2 + … + n)² = (n(n+1)/2)²")
    blank()
    result("Total rectangles", str(all_rects))
    result("Squares only", str(squares))
    result("Non-square rectangles", str(non_square_rects))
    blank()
    label(f"Verification : {all_rects} − {squares} = {non_square_rects}")


def test_shortest_paths() -> None:
    section(4, "Shortest Path Between Two Nodes")

    label("Graph type              Algorithm")
    rule()
    label("Unweighted              BFS")
    label("Weighted (positive)     Dijkstra")
    label("Negative weights        Bellman–Ford")
    label("All-pairs               Floyd–Warshall")
    blank()

    unweighted = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    dist, path = bfs_shortest_path(unweighted, "A", "D")
    label("▸ BFS  (unweighted graph)")
    result("Source → Destination", "A → D")
    result("Shortest distance", f"{int(dist)} hops")
    result("Path", " → ".join(path))
    blank()

    weighted = {
        "A": [("B", 4.0), ("C", 2.0)],
        "B": [("D", 5.0)],
        "C": [("B", 1.0), ("D", 8.0)],
        "D": [],
    }
    dist, path = dijkstra_shortest_path(weighted, "A", "D")
    label("▸ Dijkstra  (non-negative weights)")
    result("Source → Destination", "A → D")
    result("Shortest distance", str(dist))
    result("Path", " → ".join(path))
    blank()

    with_negative = {
        "A": [("B", 1.0), ("C", 4.0)],
        "B": [("C", -2.0), ("D", 3.0)],
        "C": [("D", 1.0)],
        "D": [],
    }
    dist, path = bellman_ford_shortest_path(with_negative, "A", "D")
    label("▸ Bellman–Ford  (negative weights allowed)")
    result("Source → Destination", "A → D")
    result("Shortest distance", str(dist))
    result("Path", " → ".join(path))
    blank()

    inf = float("inf")
    labels = ["A", "B", "C", "D"]
    matrix = [
        [0, 3, inf, 7],
        [8, 0, 2, inf],
        [5, inf, 0, 1],
        [2, inf, inf, 0],
    ]
    dist_matrix, paths = floyd_warshall_all_pairs(matrix, labels)
    label("▸ Floyd–Warshall  (all-pairs shortest paths)")
    result("Source → Destination", "A → D")
    result("Shortest distance", str(dist_matrix[0][3]))
    result("Path", " → ".join(paths[("A", "D")]))


def build_output() -> str:
    buffer = StringIO()
    original_stdout = sys.stdout
    sys.stdout = buffer
    try:
        print_banner()
        test_lemon_watchman()
        test_chessboard_squares()
        test_chessboard_rectangles()
        test_shortest_paths()
        print_footer()
    finally:
        sys.stdout = original_stdout
    return buffer.getvalue()


def print_banner() -> None:
    rule("═")
    print("  CLASSIC INTERVIEW PUZZLES & GRAPH ALGORITHMS")
    print("  Python Implementations — Sample Output")
    rule("═")


def print_footer() -> None:
    print()
    rule("═")
    print("  All test cases completed successfully.")
    rule("═")
    print()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(build_output(), end="")


if __name__ == "__main__":
    main()
