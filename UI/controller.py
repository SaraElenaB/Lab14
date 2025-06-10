import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._storeSelected = None
        self._nodeSelected = None

    #--------------------------------------------------------------------------------------------------------------------------------
    def fillDDStore(self): #potevo salvare anche solo come str

        stores= self._model.getAllStore()
        for s in stores:
            self._view._ddStore.options.append( ft.dropdown.Option( key=s.store_id,
                                                                    data=s,
                                                                    on_click= self._choiceDDStore))
        print([opt.key for opt in self._view._ddStore.options])

    def _choiceDDStore(self, e):
        self._storeSelected = e.control.data


    def fillDDNode(self, storeId):

        nodes= self._model.getAllNodes(storeId)
        for n in nodes:
            self._view._ddNode.options.append( ft.dropdown.Option( key=n.order_id,
                                                                   data=n,
                                                                   on_click= self._choiceDDNode))

    def _choiceDDNode(self, e):
        self._nodeSelected = e.control.data

    # --------------------------------------------------------------------------------------------------------------------------------
    def handleCreaGrafo(self, e):

        numGiorniMax = self._view._txtIntK.value
        storeValue = self._view._ddStore.value
        store = self._model.getStore(int(storeValue))

        print(f"Valore selezionato nel dropdown: {storeValue}")
        print(f"Tutti gli store nella mappa: {self._model._mapStores}")

        if numGiorniMax is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione, inserire un numero massimo di giorni", color="red"))
            self._view.update_page()
            return

        try:
            intNumGiorniMax = int(numGiorniMax)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione, il valore inserito non è un numero", color="red"))
            self._view.update_page()
            return

        if store is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione, selezionare uno store per continuare", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(store.store_id, intNumGiorniMax)
        self.fillDDNode(store.store_id)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append( ft.Text(f"Grafo correttamente creato:"))
        numNodi, numArchi = self._model.getGrafoDetails()
        self._view.txt_result.controls.append( ft.Text(f"Numero di nodi: {numNodi} \nNumero di archi: {numArchi}"))
        self._view.update_page()

    # --------------------------------------------------------------------------------------------------------------------------------
    def handleCerca(self, e):

        sourceid = self._view._ddNode.value

        if sourceid is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text( f"Attenzione, selezionare un nodo di partenza!", color="red"))
            self._view.update_page()
            return

        longestPath = self._model.getLongestPath(sourceid)
        self._view.txt_result.controls.append(ft.Text( f"Nodo di partenza: {sourceid}"))

        for n in longestPath[1:]:
            self._view.txt_result.controls.append( ft.Text(n) )
        self._view.update_page()

    # --------------------------------------------------------------------------------------------------------------------------------
    def handleRicorsione(self, e):

        sourceid = self._view._ddNode.value

        if sourceid is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, selezionare un nodo di partenza!", color="red"))
            self._view.update_page()
            return

        bestPath, bestCost = self._model.getBestCamminoPesoMaggiore(sourceid)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append( ft.Text(f"Il percorso migliore ha costo: {bestCost}"))
        for nodo in bestPath:
            self._view.txt_result.controls.append( ft.Text(nodo) )
        self._view.update_page()

#--------------------------------------------------------------------------------------------------------------------------------



