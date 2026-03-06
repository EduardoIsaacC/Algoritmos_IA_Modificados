import networkx as nx
import matplotlib.pyplot as plt
import heapq
import time

# -----------------------------
# PROBLEMA
# Empresa de logística que busca la ruta más corta
# desde el almacén central hasta el cliente.
# -----------------------------

G = nx.Graph()

edges = [
("Almacen","A",4),
("Almacen","B",2),
("A","C",3),
("B","C",1),
("B","D",7),
("C","D",3),
("C","Cliente",6),
("D","Cliente",2)
]

G.add_weighted_edges_from(edges)

pos = nx.spring_layout(G)

def dibujar(visitados=[], camino=[]):

    plt.clf()

    nx.draw(G,pos,node_color="lightgray",node_size=2000,with_labels=True)

    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

    nx.draw_networkx_nodes(G,pos,nodelist=visitados,node_color="orange")

    if camino:
        ruta_edges = list(zip(camino,camino[1:]))
        nx.draw_networkx_edges(G,pos,edgelist=ruta_edges,width=4,edge_color="red")

    plt.title("Dijkstra - Ruta de Almacenes")
    plt.pause(1)


def dijkstra(inicio, destino):

    dist = {n:float('inf') for n in G.nodes}
    prev = {n:None for n in G.nodes}

    dist[inicio] = 0

    pq = [(0,inicio)]

    visitados = []

    while pq:

        d,u = heapq.heappop(pq)

        if u not in visitados:

            visitados.append(u)
            dibujar(visitados)

            if u == destino:
                break

            for v in G.neighbors(u):

                peso = G[u][v]['weight']
                nueva = d + peso

                if nueva < dist[v]:

                    dist[v] = nueva
                    prev[v] = u
                    heapq.heappush(pq,(nueva,v))

    camino = []
    nodo = destino

    while nodo:
        camino.append(nodo)
        nodo = prev[nodo]

    camino.reverse()

    dibujar(visitados,camino)

    print("Ruta óptima:",camino)
    print("Distancia:",dist[destino])


plt.figure()

dijkstra("Almacen","Cliente")

plt.show()