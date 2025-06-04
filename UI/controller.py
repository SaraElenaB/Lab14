import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._storeSelected = None
        self._nodeSelected = None

    def fillDDStore(self):

        stores= self._model.getAllStore()
        for s in stores:
            self._view._ddStore.options.append( ft.dropdown.Option( key=s.store_id,
                                                                    data=s,
                                                                    on_click= self._readStore))

    def _readStore(self, e):
        self._storeSelected = e.control.data

    def fillDDNode(self, storeId):

        nodes= self._model.getAllNodes(storeId)
        for n in nodes:
            self._view._ddNode.options.append( ft.dropdown.Option( key=n.order_id,
                                                                    data=n,
                                                                    on_click= self._readNodes))

    def _readNodes(self, e):
        self._nodeSelected = e.control.data


    def handleCreaGrafo(self, e):

        numGiorniMax = self._view._txtIntK.value
        store = self._view._ddStore.value

        if numGiorniMax is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( f"Attenzione, inserire un numero massimo di giorni", color="red")
            self._view.update_page()
            return

        try:
            intNumGiorniMax = int(numGiorniMax)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(f"Attenzione, il valore inserito non è un numero", color="red")
            self._view.update_page()
            return

        if store is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( f"Attenzione, selezionare uno store per continuare", color="red")
            self._view.update_page()
            return

        self._model.buildGraph(store.store_id, intNumGiorniMax)
        self.fillDDNode(store.store_id)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(f"Grafo correttamente creato:")
        numNodi, numArchi = self._model.getGrafoDetails()
        self._view.txt_result.controls.append(f"Numero di nodi: {numNodi} \nNumero di archi: {numArchi}")

        # nodoPartenza = self._view._ddNode.value
        #
        # if numGiorniMax is None:
        #     self._view.txt_result.controls.clear()
        #     self._view.txt_result.controls.append( f"Attenzione, inserire un nodo di partenza per continuare", color="red")
        #     self._view.update_page()
        #     return

        self._view.update_page()
        #longestPath = self._model.getLongestPath(nodoPartenza)







    def handleCerca(self, e):
        pass

    def handleRicorsione(self, e):
        pass
