"""Shortest path algorithms for graphs."""

from collections import deque
from typing import Dict, Hashable, List, Optional, Tuple, Union

Graph = Dict[Hashable, List[Tuple[Hashable, float]]]
WeightMatrix = List[List[float]]
PathResult = Tuple[Optional[float], Optional[List[Hashable]]]


def bfs_shortest_path(
    graph: Dict[Hashable, List[Hashable]],
    source: Hashable,
    destination: Hashable,
) -> PathResult:
    """Unweighted graph: BFS returns hop count and path."""
    if source == destination:
        return 0.0, [source]

    visited = {source}
    queue = deque([(source, [source])])

    while queue:
        node, path = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor in visited:
                continue
            new_path = path + [neighbor]
            if neighbor == destination:
                return float(len(new_path) - 1), new_path
            visited.add(neighbor)
            queue.append((neighbor, new_path))

    return None, None


def dijkstra_shortest_path(
    graph: Graph,
    source: Hashable,
    destination: Hashable,
) -> PathResult:
    """Weighted graph with non-negative weights: Dijkstra's algorithm."""
    import heapq

    if source == destination:
        return 0.0, [source]

    dist: Dict[Hashable, float] = {source: 0.0}
    previous: Dict[Hashable, Optional[Hashable]] = {source: None}
    heap: List[Tuple[float, Hashable]] = [(0.0, source)]

    while heap:
        current_dist, node = heapq.heappop(heap)
        if current_dist > dist.get(node, float("inf")):
            continue
        if node == destination:
            break
        for neighbor, weight in graph.get(node, []):
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights")
            new_dist = current_dist + weight
            if new_dist < dist.get(neighbor, float("inf")):
                dist[neighbor] = new_dist
                previous[neighbor] = node
                heapq.heappush(heap, (new_dist, neighbor))

    if destination not in dist:
        return None, None

    path: List[Hashable] = []
    current: Optional[Hashable] = destination
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    return dist[destination], path


def bellman_ford_shortest_path(
    graph: Graph,
    source: Hashable,
    destination: Hashable,
) -> PathResult:
    """Weighted graph (may have negative weights): Bellman-Ford algorithm."""
    nodes = set(graph.keys())
    for neighbors in graph.values():
        for neighbor, _ in neighbors:
            nodes.add(neighbor)

    dist: Dict[Hashable, float] = {node: float("inf") for node in nodes}
    previous: Dict[Hashable, Optional[Hashable]] = {node: None for node in nodes}
    dist[source] = 0.0

    edges = [
        (u, v, w)
        for u, neighbors in graph.items()
        for v, w in neighbors
    ]

    for _ in range(len(nodes) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                previous[v] = u
                updated = True
        if not updated:
            break

    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    if dist[destination] == float("inf"):
        return None, None

    path: List[Hashable] = []
    current: Optional[Hashable] = destination
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    return dist[destination], path


def floyd_warshall_all_pairs(
    matrix: WeightMatrix,
    node_labels: Optional[List[Hashable]] = None,
) -> Tuple[WeightMatrix, Dict[Tuple[Hashable, Hashable], List[Hashable]]]:
    """
    All-pairs shortest paths using Floyd-Warshall.

    matrix[i][j] is the weight from node i to node j (use inf for no edge).
    """
    n = len(matrix)
    labels = node_labels or list(range(n))
    if len(labels) != n:
        raise ValueError("node_labels length must match matrix size")

    dist = [row[:] for row in matrix]
    next_node: Dict[Tuple[Hashable, Hashable], Optional[Hashable]] = {}

    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float("inf"):
                next_node[(labels[i], labels[j])] = labels[j]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[(labels[i], labels[j])] = next_node[(labels[i], labels[k])]

    paths: Dict[Tuple[Hashable, Hashable], List[Hashable]] = {}
    for i in range(n):
        for j in range(n):
            if i == j:
                paths[(labels[i], labels[j])] = [labels[i]]
                continue
            if dist[i][j] == float("inf"):
                continue
            path = [labels[i]]
            current = labels[i]
            while current != labels[j]:
                current = next_node[(current, labels[j])]
                path.append(current)
            paths[(labels[i], labels[j])] = path

    return dist, paths
