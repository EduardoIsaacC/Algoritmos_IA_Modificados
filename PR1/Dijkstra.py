# dijkstra_anim_es.py
import heapq
from typing import Dict, List, Tuple, Optional

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

GrafoDirigido = Dict[str, List[Tuple[str, float]]]


def dijkstra_pasos(grafo: GrafoDirigido, inicio: str, objetivo: str):
    """
    Dijkstra para ruta más rápida (costos >= 0).
    Devuelve:
    - orden_extraidos: nodos sacados del heap (orden de procesamiento)
    - ruta_final: ruta óptima (lista de nodos)
    - costo_final: costo mínimo
    """
    distancias: Dict[str, float] = {inicio: 0.0}
    padre: Dict[str, Optional[str]] = {inicio: None}

    cola: List[Tuple[float, str]] = [(0.0, inicio)]
    orden_extraidos: List[str] = []

    while cola:
        costo_actual, nodo = heapq.heappop(cola)

        # Si esta entrada es “vieja” (peor que la mejor conocida), se ignora
        if costo_actual > distancias.get(nodo, float("inf")):
            continue

        orden_extraidos.append(nodo)

        if nodo == objetivo:
            break

        for vecino, peso in grafo.get(nodo, []):
            nuevo_costo = costo_actual + peso
            if nuevo_costo < distancias.get(vecino, float("inf")):
                distancias[vecino] = nuevo_costo
                padre[vecino] = nodo
                heapq.heappush(cola, (nuevo_costo, vecino))

    if objetivo not in distancias:
        return orden_extraidos, [], float("inf")

    # Reconstruir ruta usando "padre"
    ruta = []
    actual = objetivo
    while actual is not None:
        ruta.append(actual)
        actual = padre[actual]
    ruta.reverse()

    return orden_extraidos, ruta, distancias[objetivo]


def dibujar_base(ax, posiciones, aristas, titulo):
    ax.clear()
    ax.set_title(titulo)
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")

    # Dibujar aristas
    for (u, v, w) in aristas:
        x1, y1 = posiciones[u]
        x2, y2 = posiciones[v]
        ax.plot([x1, x2], [y1, y2], linewidth=1)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my, str(w), fontsize=9)

    # Dibujar nodos
    for nodo, (x, y) in posiciones.items():
        ax.scatter([x], [y], s=520)
        ax.text(x, y, nodo, ha="center", va="center", fontweight="bold")


def resaltar_nodo(ax, posiciones, nodo):
    x, y = posiciones[nodo]
    ax.scatter([x], [y], s=900)


def resaltar_aristas(ax, posiciones, lista_aristas, grosor=7):
    for (u, v, _) in lista_aristas:
        x1, y1 = posiciones[u]
        x2, y2 = posiciones[v]
        ax.plot([x1, x2], [y1, y2], linewidth=grosor)


def main():
    # Caso vida diaria: ruta más rápida (minutos)
    grafo: GrafoDirigido = {
        "Casa": [("Oxxo", 6), ("Gym", 12)],
        "Oxxo": [("Trabajo", 18), ("Super", 8)],
        "Gym": [("Trabajo", 10)],
        "Super": [("Trabajo", 9), ("Casa", 7)],
        "Trabajo": []
    }

    # Coordenadas para visualizar
    posiciones = {
        "Casa": (0, 0),
        "Oxxo": (2, 1),
        "Super": (2, -1),
        "Gym": (4, 1),
        "Trabajo": (6, 0),
    }

    # Aristas para dibujo (no dirigido solo para mostrar)
    aristas = [
        ("Casa", "Oxxo", 6),
        ("Casa", "Gym", 12),
        ("Oxxo", "Trabajo", 18),
        ("Oxxo", "Super", 8),
        ("Gym", "Trabajo", 10),
        ("Super", "Trabajo", 9),
        ("Super", "Casa", 7),
    ]

    orden, ruta, costo = dijkstra_pasos(grafo, "Casa", "Trabajo")

    print("\nResultado (entre la data):")
    print("Tiempo mínimo (min):", costo)
    print("Ruta óptima:", " -> ".join(ruta))

    fig, ax = plt.subplots()

    def actualizar(i):
        titulo = f"Dijkstra | Paso {i+1}/{len(orden)} | Tiempo mínimo final: {costo} min"
        dibujar_base(ax, posiciones, aristas, titulo)

        # Resaltar nodos procesados
        for k in range(i + 1):
            resaltar_nodo(ax, posiciones, orden[k])

        # Al final resaltar la ruta óptima
        if i == len(orden) - 1 and ruta:
            aristas_ruta = []
            for a, b in zip(ruta, ruta[1:]):
                w = next(w for (u, v, w) in aristas if (u == a and v == b) or (u == b and v == a))
                aristas_ruta.append((a, b, w))
            resaltar_aristas(ax, posiciones, aristas_ruta, grosor=8)
            ax.text(0.02, 0.02, "Ruta: " + " -> ".join(ruta), transform=ax.transAxes)

    anim = FuncAnimation(fig, actualizar, frames=max(1, len(orden)), interval=900, repeat=False)
    plt.show()


if __name__ == "__main__":
    main()