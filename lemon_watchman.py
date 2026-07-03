"""Lemon/Watchman/Farm puzzle: work backwards from the final lemon."""


def initial_lemons(num_gates: int) -> int:
    """
    At each gate a watchman takes half of the lemons plus one more.
    After passing all gates, exactly one lemon remains.

    Working backwards: if x lemons remain after a gate, there were 2(x + 1) before it.
    """
    if num_gates < 0:
        raise ValueError("num_gates must be non-negative")

    lemons = 1
    for _ in range(num_gates):
        lemons = 2 * (lemons + 1)
    return lemons
