import copy
import itertools

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):

        self._grafo= nx.DiGraph()
        self._stores = DAO.getAllStore()

        self._mapStores = {}
        for s in self._stores:
            self._mapStores[s.store_id] = s

        self.nodes = []
        self._longestPath= []
        self._bestPath = []
        self._bestCost = 0

    # --------------------------------------------------------------------------------------------------------------------------------
    def getStore(self, idStore):
        print(f"Cerco store con ID: {idStore} (tipo: {type(idStore)})")  #ADORO!!!
        return self._mapStores.get(idStore)

    def getAllStore(self):
        return DAO.getAllStore()

    def getAllNodes(self, storeId):
        return DAO.getAllNodes(storeId)

    # --------------------------------------------------------------------------------------------------------------------------------
    def buildGraph(self, storeId, intNumGiorniMax):

        self._grafo.clear()
        self.nodes = DAO.getAllNodes(storeId)
        self._grafo.add_nodes_from(self.nodes)

        self._mapNodes = {}
        for n in self.nodes:
            self._mapNodes[n.order_id] = n

        for n1, n2 in itertools.combinations(self.nodes, 2):
            diff_days1 = (n1.order_date - n2.order_date).days
            if 0 < diff_days1 < intNumGiorniMax:
                peso1 = DAO.getAllWeight(n1.order_id, n2.order_id)
                self._grafo.add_edge(n1, n2, weight=peso1[0])  #weight=peso1 --> lista
                                                               #weight=peso1[0] --> int

            diff_days2 = (n2.order_date - n1.order_date).days
            if 0 < diff_days2 < intNumGiorniMax:
                peso2 = DAO.getAllWeight(n2.order_id, n1.order_id)
                self._grafo.add_edge(n2, n1, weight=peso2[0])

        print(f"Num nodi: {len(self._grafo.nodes)} \nNum archi:{len(self._grafo.edges)}")
        return self._grafo

    # --------------------------------------------------------------------------------------------------------------------------------
    def getGrafoDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    # --------------------------------------------------------------------------------------------------------------------------------
    def getLongestPath(self, nodoId):

        source = self._mapNodes[int(nodoId)]
        self._longestPath = []
        parziale = [source]
        nodi = list( nx.dfs_tree(self._grafo, source))
        self._ricorsione1(parziale, nodi)
        return self._longestPath

    def _ricorsione1(self, parziale, nodi):
        #terminale
        if len(parziale) > len(self._longestPath):
            self._longestPath = copy.deepcopy(parziale)

        #ricorsione
        for node in nodi:
            if node not in parziale:
                parziale.append(node)
                self._ricorsione1(parziale, nodi)
                parziale.pop()

    # --------------------------------------------------------------------------------------------------------------------------------
    def getBestCamminoPesoMaggiore(self, sourceId):

        source = self._mapNodes[int(sourceId)]
        self._bestPath = []
        self._bestCost = 0
        parziale = [source]

        # serve a iniziare il processo con un cammino già con due nodi, così che dentro la ricorsione puoi fare
        # confronti con parziale[-2]parziale[-1]
        vicini = self._grafo.neighbors(source)
        for v in vicini:
            parziale.append(v)
            self._ricorsione2(parziale)
            parziale.pop()

        return self._bestPath, self._bestCost

    def _ricorsione2(self, parziale):
        #terminale
        costo = self.calcolaCosto(parziale)
        if costo > self._bestCost:
            self._bestCost = costo
            self._bestPath = copy.deepcopy(parziale)

        # ricorsione --> continua la costruzione del cammino ricorsivamente, ma per funzionare ha bisogno che il cammino abbia
        # almeno 2 nodi per confrontare il peso
        for nodo in self._grafo.neighbors( parziale[-1]):
            #vincoli
            if (nodo not in parziale and
                self._grafo[parziale[-2]][parziale[-1]]["weight"] >
                self._grafo[parziale[-1]][nodo]["weight"]):

                parziale.append(nodo)
                self._ricorsione2(parziale)
                parziale.pop()

    # --------------------------------------------------------------------------------------------------------------------------------
    def calcolaCosto(self, listaDiNodi):

        costo=0
        for i in range(len(listaDiNodi) -1):
            costo += self._grafo[listaDiNodi[i]][listaDiNodi[i+1]]["weight"]

        return costo

    #--------------------------------------------------------------------------------------------------------------------------------





if __name__ == "__main__":
    m= Model()

    print( m._mapStores)

    grafo = m.buildGraph(1,5)
    print(f"Grafo: {grafo}")