import itertools

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):

        self._grafo= nx.DiGraph()
        self.nodes = []


    def getAllStore(self):
        return DAO.getAllStore()

    def buildGraph(self, storeId, intNumGiorniMax):

        self._grafo.clear()
        self.nodes = DAO.getAllNodes(storeId)
        self._grafo.add_nodes_from(self.nodes)

        for n1, n2 in itertools.combinations(self.nodes, 2):
            diff_days1 = (n1.order_date - n2.order_date).days
            if 0 < diff_days1 < intNumGiorniMax:
                peso1 = DAO.getAllWeight(n1.order_id, n2.order_id)
                self._grafo.add_edge(n1, n2, weight=peso1)


            diff_days2 = (n2.order_date - n1.order_date).days
            if 0 < diff_days2 < intNumGiorniMax:
                peso2 = DAO.getAllWeight(n2.order_id, n1.order_id)
                self._grafo.add_edge(n2, n1, weight=peso2)

        print(f"Num nodi: {len(self._grafo.nodes)} \nNum archi:{len(self._grafo.edges)}")
        return self._grafo

    def getGrafoDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getLongestPath(self, nodo):
        pass








if __name__ == "__main__":
    m= Model()
    grafo = m.buildGraph(1,5)
    print(f"Grafo: {grafo}")