import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        self._model.build_graph()

    def handleDettagli(self, e):
        pass

    def handlePercorso(self, e):
        pass

    def fill_dd_year(self):
        years = self._model.get_years()
        years_dd = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options = years_dd
        self._view.update_page()

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

    def read_dd_teams(self, e):
        if e.control.data is None:
            self.selected_team = None
        else:
            self.selected_team = e.control.data


