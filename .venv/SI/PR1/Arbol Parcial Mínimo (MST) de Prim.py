# prim_anim_es.py
import heapq
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

GrafoNoDirigido = Dict[str, List[Tuple[str, float]]]


def prim_pasos(grafo: GrafoNoDirigido, inicio: str):
    """
    Prim para Árbol de Expansión Mínima (MST).
    Devuelve:
    - pasos: lista con (aristas_elegidas, costo_subtotal, nodos_visitados)
    - costo_total
    """
    visitados = set([inicio])
    cola: List[Tuple[float, str, str]] = []

    for v, w in grafo.get(inicio, []):
        heapq.heappush(cola, (w, inicio, v))

    aristas_elegidas = []
    costo_total = 0.0
    pasos = []

    while cola and len(visitados) < len(grafo):
        w, u, v = heapq.heappop(cola)
        if v in visitados:
            continue

        visitados.add(v)
        aristas_elegidas.append((u, v, w))
        costo_total += w

        pasos.append((aristas_elegidas.copy(), costo_total, visitados.copy()))

        for siguiente, w2 in grafo.get(v, []):
            if siguiente not in visitados:
                heapq.heappush(cola, (w2, v, siguiente))

    if len(visitados) != len(grafo):
        return [], float("inf")

    return pasos, costo_total


def dibujar_base(ax, posiciones, aristas, titulo):
    ax.clear()
    ax.set_title(titulo)
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")

    for (u, v, w) in aristas:
        x1, y1 = posiciones[u]
        x2, y2 = posiciones[v]
        ax.plot([x1, x2], [y1, y2], linewidth=1)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my, str(w), fontsize=9)

    for nodo, (x, y) in posiciones.items():
        ax.scatter([x], [y], s=520)
        ax.text(x, y, nodo, ha="center", va="center", fontweight="bold")


def resaltar_aristas(ax, posiciones, aristas, grosor=7):
    for (u, v, _) in aristas:
        x1, y1 = posiciones[u]
        x2, y2 = posiciones[v]
        ax.plot([x1, x2], [y1, y2], linewidth=grosor)


def resaltar_nodos(ax, posiciones, nodos):
    for nodo in nodos:
        x, y = posiciones[nodo]
        ax.scatter([x], [y], s=900)


def main():
    # Caso vida diaria: cableado mínimo (metros o $)
    taller: GrafoNoDirigido = {
        "PLC": [("Sensor1", 7), ("Sensor2", 4), ("HMI", 6)],
        "Sensor1": [("PLC", 7), ("Motor", 3)],
        "Sensor2": [("PLC", 4), ("Motor", 8), ("Camara", 5)],
        "HMI": [("PLC", 6), ("Camara", 2)],
        "Motor": [("Sensor1", 3), ("Sensor2", 8), ("Camara", 4)],
        "Camara": [("Sensor2", 5), ("HMI", 2), ("Motor", 4)],
    }

    posiciones = {
        "PLC": (0, 0),
        "Sensor1": (2, 1.5),
        "Sensor2": (2, -1.5),
        "HMI": (4, 1.5),
        "Motor": (5, -1.2),
        "Camara": (6, 1.0),
    }

    aristas = [
        ("PLC", "Sensor1", 7),
        ("PLC", "Sensor2", 4),
        ("PLC", "HMI", 6),
        ("Sensor1", "Motor", 3),
        ("Sensor2", "Motor", 8),
        ("Sensor2", "Camara", 5),
        ("HMI", "Camara", 2),
        ("Motor", "Camara", 4),
    ]

    pasos, costo_total = prim_pasos(taller, "PLC")
    if not pasos:
        print("El grafo está desconectado: no hay MST.")
        return

    print("\nResultado (entre la data):")
    print("Costo mínimo total de cableado:", costo_total)
    print("Conexiones elegidas (MST):", pasos[-1][0])

    fig, ax = plt.subplots()

    def actualizar(i):
        elegidas, subtotal, visitados = pasos[i]
        titulo = f"Prim (MST) | Paso {i+1}/{len(pasos)} | Subtotal={subtotal:.1f} | Final={costo_total:.1f}"
        dibujar_base(ax, posiciones, aristas, titulo)
        resaltar_aristas(ax, posiciones, elegidas, grosor=8)
        resaltar_nodos(ax, posiciones, visitados)

    anim = FuncAnimation(fig, actualizar, frames=len(pasos), interval=900, repeat=False)
    plt.show()


if __name__ == "__main__":
    main()