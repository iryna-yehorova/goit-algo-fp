import heapq
import itertools
import math


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adjacency = {}

    def add_vertex(self, vertex):
        self.adjacency.setdefault(vertex, [])

    def add_edge(self, start, end, weight):
        if not isinstance(weight, (int, float)) or not math.isfinite(weight) or weight < 0:
            raise ValueError("Вага ребра має бути невід'ємним скінченним числом")
        self.add_vertex(start)
        self.add_vertex(end)
        self.adjacency[start].append((end, weight))
        if not self.directed:
            self.adjacency[end].append((start, weight))


def dijkstra(graph, start):
    if start not in graph.adjacency:
        raise ValueError(f"Початкової вершини {start!r} немає у графі")

    distances = {vertex: math.inf for vertex in graph.adjacency}
    previous = {vertex: None for vertex in graph.adjacency}
    distances[start] = 0

    counter = itertools.count()
    heap = [(0, next(counter), start)]

    while heap:
        current_distance, _, vertex = heapq.heappop(heap)
        if current_distance > distances[vertex]:
            continue

        for neighbor, weight in graph.adjacency[vertex]:
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = vertex
                heapq.heappush(heap, (new_distance, next(counter), neighbor))

    return distances, previous


def shortest_path(previous, start, target):
    path = []
    vertex = target
    while vertex is not None:
        path.append(vertex)
        if vertex == start:
            return path[::-1]
        vertex = previous[vertex]
    return []


if __name__ == "__main__":
    graph = Graph()
    for start, end, weight in (
        ("A", "B", 4), ("A", "C", 2), ("B", "C", 1),
        ("B", "D", 5), ("C", "D", 8), ("C", "E", 10),
        ("D", "E", 2), ("D", "F", 6), ("E", "F", 3),
    ):
        graph.add_edge(start, end, weight)
    graph.add_vertex("G")

    source = "A"
    distances, previous = dijkstra(graph, source)
    for vertex, distance in distances.items():
        path = shortest_path(previous, source, vertex)
        route = " → ".join(path) if path else "шляху немає"
        print(f"{source} → {vertex}: відстань {distance}, шлях: {route}")
