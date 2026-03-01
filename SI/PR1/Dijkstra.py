import heapq
from typing import Dict, List, Tuple, Optional

Graph = Dict[str, List[Tuple[str, float]]]  # nodo -> [(vecino, costo), ...]

def dijkstra_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[float, List[str]]:
    """
    Dijkstra: encuentra el costo mínimo y el camino (ruta) de start a goal.
    Aplicación: ruta más rápida para entrega (minutos), transporte, etc.
    """
    # dist[nodo] = mejor costo conocido desde start
    dist: Dict[str, float] = {start: 0.0}
    parent: Dict[str, Optional[str]] = {start: None}

    pq: List[Tuple[float, str]] = [(0.0, start)]  # (costo acumulado, nodo)

    while pq:
        current_cost, node = heapq.heappop(pq)

        # Si sacamos un estado viejo (más caro) lo ignoramos
        if current_cost > dist.get(node, float("inf")):
            continue

        if node == goal:
            break

        for neighbor, w in graph.get(node, []):
            new_cost = current_cost + w
            if new_cost < dist.get(neighbor, float("inf")):
                dist[neighbor] = new_cost
                parent[neighbor] = node
                heapq.heappush(pq, (new_cost, neighbor))

    if goal not in dist:
        return float("inf"), []

    # reconstruir ruta
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    return dist[goal], path


if __name__ == "__main__":
    # Grafo de "colonias/sucursales" con tiempos (min)
    city_graph: Graph = {
        "Casa": [("Oxxo", 6), ("Gym", 12)],
        "Oxxo": [("Trabajo", 18), ("Super", 8)],
        "Gym": [("Trabajo", 10)],
        "Super": [("Trabajo", 9), ("Casa", 7)],
        "Trabajo": []
    }

    cost, route = dijkstra_shortest_path(city_graph, "Casa", "Trabajo")
    print("Tiempo mínimo (min):", cost)
    print("Ruta:", " -> ".join(route))