import heapq
from typing import Dict, List, Tuple

# Para Prim, es cómodo un grafo no dirigido: si A-B existe, también B-A
UGraph = Dict[str, List[Tuple[str, float]]]

def prim_mst(graph: UGraph, start: str) -> Tuple[float, List[Tuple[str, str, float]]]:
    """
    Prim: construye un Árbol de Expansión Mínima (MST).
    Aplicación: minimizar cableado/tubería/costo conectando todos los nodos.
    Retorna:
      - costo_total
      - lista de aristas (u, v, w) del MST
    """
    visited = set([start])
    mst_edges: List[Tuple[str, str, float]] = []
    total_cost = 0.0

    # cola con aristas candidatas: (peso, u, v)
    pq: List[Tuple[float, str, str]] = []
    for v, w in graph.get(start, []):
        heapq.heappush(pq, (w, start, v))

    while pq and len(visited) < len(graph):
        w, u, v = heapq.heappop(pq)
        if v in visited:
            continue

        # Tomamos la arista más barata que conecta un nuevo nodo
        visited.add(v)
        mst_edges.append((u, v, w))
        total_cost += w

        # Agregar nuevas aristas desde v
        for nxt, w2 in graph.get(v, []):
            if nxt not in visited:
                heapq.heappush(pq, (w2, v, nxt))

    # Si no se visitaron todos, el grafo estaba desconectado
    if len(visited) != len(graph):
        return float("inf"), []

    return total_cost, mst_edges


if __name__ == "__main__":
    # "Estaciones" en un taller con costo de cable (m o $)
    lab: UGraph = {
        "PLC": [("Sensor1", 7), ("Sensor2", 4), ("HMI", 6)],
        "Sensor1": [("PLC", 7), ("Motor", 3)],
        "Sensor2": [("PLC", 4), ("Motor", 8), ("Camara", 5)],
        "HMI": [("PLC", 6), ("Camara", 2)],
        "Motor": [("Sensor1", 3), ("Sensor2", 8), ("Camara", 4)],
        "Camara": [("Sensor2", 5), ("HMI", 2), ("Motor", 4)]
    }

    cost, edges = prim_mst(lab, "PLC")
    print("Costo mínimo total:", cost)
    print("Aristas del MST:")
    for u, v, w in edges:
        print(f"  {u} --({w})--> {v}")