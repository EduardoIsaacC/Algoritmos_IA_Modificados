from typing import List, Tuple, Dict

Edge = Tuple[str, str, float]  # (u, v, w)

class DSU:
    def __init__(self, nodes):
        self.parent = {x: x for x in nodes}
        self.rank = {x: 0 for x in nodes}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

def kruskal_spanning_tree(nodes: List[str], edges: List[Edge], maximize: bool = False) -> Tuple[float, List[Edge]]:
    """
    Kruskal: construye árbol de expansión.
    - maximize=False -> MST (mínimo costo)
    - maximize=True  -> MaxST (máximo costo)
    """
    dsu = DSU(nodes)
    chosen: List[Edge] = []
    total = 0.0

    edges_sorted = sorted(edges, key=lambda e: e[2], reverse=maximize)

    for u, v, w in edges_sorted:
        if dsu.union(u, v):
            chosen.append((u, v, w))
            total += w
            if len(chosen) == len(nodes) - 1:
                break

    if len(chosen) != len(nodes) - 1:
        return float("inf"), []

    return total, chosen


if __name__ == "__main__":
    # Ejemplo: conectar sucursales.
    # w = costo de enlace (para MST)
    # si quisieras MaxST, interpreta w como "capacidad/beneficio"
    nodes = ["A", "B", "C", "D", "E"]
    edges: List[Edge] = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 7),
        ("C", "D", 3),
        ("C", "E", 6),
        ("D", "E", 5),
    ]

    min_cost, min_tree = kruskal_spanning_tree(nodes, edges, maximize=False)
    print("MST (mínimo costo):", min_cost, min_tree)

    max_cost, max_tree = kruskal_spanning_tree(nodes, edges, maximize=True)
    print("MaxST (máximo costo):", max_cost, max_tree)