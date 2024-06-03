import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.selected_team = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dd_year(self):
        years = self._model.get_years()
        years_dd = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options = years_dd
        self._view.update_page()

    def read_dd_teams(self, e):
        if e.control.data is None:
            self.selected_team = None
        else:
            self.selected_team = e.control.data

    def handle_dd_selection(self, e):
        year = self._view._ddAnno.value
        teams = self._model.get_teams_of_year(year)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Nel {year} hanno giocato {len(teams)} squadre"))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode}"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data=t,
                                                                    text=t.teamCode,
                                                                    on_click=self.read_dd_teams))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        if self._view._ddAnno.value is None:
            self._view.create_alert("Seleziona un anno")
            return
        year = self._view._ddAnno.value
        self._model.build_graph(year)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        n, a = self._model.get_graph_details()
        self._view._txt_result.controls.append(ft.Text(f"Il grafo è costituito da {n} nodi e {a} archi."))
        self._view.update_page()

    def handleDettagli(self, e):
        vicini = self._model.get_sorted_neighbors(self.selected_team)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {self.selected_team}"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view.update_page()

    def handlePercorso(self, e):
        self._model.get_percorso(self.selected_team)
