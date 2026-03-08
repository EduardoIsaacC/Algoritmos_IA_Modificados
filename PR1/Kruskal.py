# kruskal_mst_anim_es.py
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

Arista = Tuple[str, str, float]


class DSU:
    """
    Estructura Unión-Búsqueda (Union-Find) para detectar ciclos.
    """
    def __init__(self, nodos):
        self.padre = {x: x for x in nodos}
        self.rango = {x: 0 for x in nodos}

    def encontrar(self, x):
        while self.padre[x] != x:
            self.padre[x] = self.padre[self.padre[x]]
            x = self.padre[x]
        return x

    def unir(self, a, b):
        ra, rb = self.encontrar(a), self.encontrar(b)
        if ra == rb:
            return False

        if self.rango[ra] < self.rango[rb]:
            ra, rb = rb, ra

        self.padre[rb] = ra

        if self.rango[ra] == self.rango[rb]:
            self.rango[ra] += 1

        return True


def kruskal_pasos(nodos: List[str], aristas: List[Arista]):
    """
    Kruskal MST (mínimo costo):
    - ordena aristas por peso ascendente
    - agrega aristas si no forman ciclo
    Devuelve:
    - pasos: (aristas_elegidas, subtotal, ultima_arista, aceptada)
    - costo_total
    """
    dsu = DSU(nodos)
    ordenadas = sorted(aristas, key=lambda e: e[2])

    elegidas = []
    costo_total = 0.0
    pasos = []

    for (u, v, w) in ordenadas:
        aceptada = dsu.unir(u, v)
        if aceptada:
            elegidas.append((u, v, w))
            costo_total += w

        pasos.append((elegidas.copy(), costo_total, (u, v, w), aceptada))

        if len(elegidas) == len(nodos) - 1:
            break

    if len(elegidas) != len(nodos) - 1:
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


def main():
    # Caso vida diaria: conectar sucursales con costo mínimo
    nodos = ["A", "B", "C", "D", "E"]
    aristas: List[Arista] = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 7),
        ("C", "D", 3),
        ("C", "E", 6),
        ("D", "E", 5),
    ]

    posiciones = {
        "A": (0, 0),
        "B": (2, 1.5),
        "C": (2, -1.5),
        "D": (5, 1.0),
        "E": (6, -1.0),
    }

    pasos, costo_total = kruskal_pasos(nodos, aristas)
    if not pasos:
        print("El grafo está desconectado: no se pudo formar MST.")
        return

    print("\nResultado (entre la data):")
    print("Costo mínimo total (MST):", costo_total)
    print("Aristas elegidas:", pasos[-1][0])

    fig, ax = plt.subplots()

    def actualizar(i):
        elegidas, subtotal, (u, v, w), aceptada = pasos[i]
        estado = "ACEPTA" if aceptada else "CICLO (RECHAZA)"
        titulo = (
            f"Kruskal MST | Paso {i+1}/{len(pasos)} | Subtotal={subtotal:.1f} | "
            f"Final={costo_total:.1f} | Última: {u}-{v}({w}) {estado}"
        )

        dibujar_base(ax, posiciones, aristas, titulo)

        # Elegidas (árbol)
        resaltar_aristas(ax, posiciones, elegidas, grosor=8)

        # Última evaluada (más gruesa)
        resaltar_aristas(ax, posiciones, [(u, v, w)], grosor=12)

    anim = FuncAnimation(fig, actualizar, frames=len(pasos), interval=900, repeat=False)
    plt.show()


if __name__ == "__main__":
    main()