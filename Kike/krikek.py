import networkx as nx
import matplotlib.pyplot as plt
import time

# -----------------------------
# PROBLEMA
# Construir una red de carreteras
# entre ciudades con el menor costo.
# -----------------------------

G = nx.Graph()

edges = [
("A","B",4),
("A","C",2),
("B","C",1),
("B","D",5),
("C","D",8),
("C","E",10),
("D","E",2),
("D","F",6),
("E","F",3)
]

G.add_weighted_edges_from(edges)

pos = nx.spring_layout(G)

def dibujar(aristas=[]):

    plt.clf()

    nx.draw(G,pos,node_color="lightyellow",node_size=2000,with_labels=True)

    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

    nx.draw_networkx_edges(G,pos,edgelist=aristas,width=4,edge_color="blue")

    plt.title("Kruskal - Construcción de carreteras")
    plt.pause(1)


class UnionFind:

    def __init__(self,nodos):
        self.parent = {n:n for n in nodos}

    def find(self,n):

        while self.parent[n] != n:
            n = self.parent[n]

        return n

    def union(self,a,b):

        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return False

        self.parent[rb] = ra
        return True


def kruskal():

    edges_sorted = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])

    uf = UnionFind(G.nodes)

    mst = []

    for u,v,data in edges_sorted:

        if uf.union(u,v):

            mst.append((u,v))

            dibujar(mst)

            time.sleep(1)

    print("MST:",mst)


plt.figure()

kruskal()

plt.show()