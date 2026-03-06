import networkx as nx
import matplotlib.pyplot as plt
import heapq
import time

# -----------------------------
# PROBLEMA
# Conectar facultades a la red principal
# de la universidad con el menor costo.
# -----------------------------

G = nx.Graph()

edges = [
("Universidad","Ingenieria",4),
("Universidad","Medicina",3),
("Hospital","Medicina",3),
("Ingenieria","Arquitectura",2),
("Ingenieria","Derecho",5),
("Medicina","Derecho",1),
("Derecho","Economia",6),
("Arquitectura","Economia",4)
]

G.add_weighted_edges_from(edges)

pos = nx.spring_layout(G)

def dibujar(aristas=[]):

    plt.clf()

    nx.draw(G,pos,node_color="lightblue",node_size=2000,with_labels=True)

    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

    nx.draw_networkx_edges(G,pos,edgelist=aristas,width=4,edge_color="green")

    plt.title("Prim - Red Universidad")
    plt.pause(1)


def prim():

    inicio = list(G.nodes)[0]

    visitados = {inicio}

    edges_mst = []

    pq = []

    for v in G.neighbors(inicio):
        peso = G[inicio][v]['weight']
        heapq.heappush(pq,(peso,inicio,v))

    while pq:

        peso,u,v = heapq.heappop(pq)

        if v not in visitados:

            visitados.add(v)
            edges_mst.append((u,v))

            dibujar(edges_mst)

            for vecino in G.neighbors(v):
                if vecino not in visitados:
                    heapq.heappush(pq,(G[v][vecino]['weight'],v,vecino))

    print("Aristas seleccionadas:",edges_mst)


plt.figure()

prim()

plt.show()