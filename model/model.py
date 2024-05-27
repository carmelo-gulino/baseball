import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.all_teams = []
        self.grafo = nx.Graph()

    def get_years(self):
        return DAO.get_all_years()

    def get_teams_of_year(self, year):
        self.all_teams = DAO.get_teams_of_year(year)
        return self.all_teams

    def build_graph(self):
        self.grafo.clear()
        if len(self.all_teams) == 0:
            print("Non ci sono squadre per il grafo")
            return
        self.grafo.add_nodes_from(self.all_teams)
        edges = list(itertools.combinations(self.all_teams, 2))   #restituisce combinazioni di coppie di nodi
        self.grafo.add_edges_from(edges)

    def print_graph_details(self):
        print(f"Grafo creato con {len(self.grafo.nodes)} nodi e {len(self.grafo.edges)} archi")
