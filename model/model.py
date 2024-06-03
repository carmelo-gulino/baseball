import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.best_obj_val = None
        self.best_path = None
        self.all_teams = []
        self.grafo = nx.Graph()
        self.teams_map = {}

    def get_years(self):
        return DAO.get_all_years()

    def get_teams_of_year(self, year):
        self.all_teams = DAO.get_teams_of_year(year)
        self.teams_map = {t.ID: t for t in self.all_teams}
        return self.all_teams

    def build_graph(self, year):
        self.grafo.clear()
        if len(self.all_teams) == 0:
            print("Non ci sono squadre per il grafo")
            return
        self.grafo.add_nodes_from(self.all_teams)
        edges = list(itertools.combinations(self.all_teams, 2))  #restituisce combinazioni di coppie di nodi
        self.grafo.add_edges_from(edges)
        teams_salaries = DAO.get_salary_of_teams(year, self.teams_map)
        for e in self.grafo.edges:
            self.grafo[e[0]][e[1]]["weight"] = teams_salaries[e[0]] + teams_salaries[e[1]]

    def print_graph_details(self):
        print(f"Grafo creato con {len(self.grafo.nodes)} nodi e {len(self.grafo.edges)} archi")

    def get_sorted_neighbors(self, nodo):
        neighbors = self.grafo.neighbors(nodo)
        n_tuples = []  #tupla in cui al nodo sono associati tutti i pesi degli archi adiacenti
        for n in neighbors:
            n_tuples.append((n, self.grafo[nodo][n]["weight"]))
        n_tuples.sort(key=lambda tupla: tupla[1], reverse=True)
        return n_tuples

    def get_graph_details(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def get_percorso(self, source):
        self.best_path = []
        self.best_obj_val = 0
        parziale = [source]
        neighbors = []  # lista di tuple (nodo, peso)
        for v in self.grafo.neighbors(parziale[-1]):
            edge_weight = self.grafo[parziale[-1]][v]["weight"]
            neighbors.append((v, edge_weight))
        neighbors.sort(key=lambda tupla: tupla[1], reverse=True)  # riordino gli archi per peso
        parziale.append(neighbors[0][0])
        self.ricorsione(parziale)
        parziale.pop()

    def ricorsione(self, parziale):
        if self.get_score(parziale) > self.best_obj_val:
            self.best_obj_val = self.get_score(parziale)
            self.best_path = copy.deepcopy(parziale)
            print(parziale)
        neighbors = []
        for v in self.grafo.neighbors(parziale[-1]):
            edge_weight = self.grafo[parziale[-1]][v]["weight"]
            neighbors.append((v, edge_weight))
        neighbors.sort(key=lambda tupla: tupla[1], reverse=True)  #riordino gli archi per peso
        for n in neighbors:
            if n[0] not in parziale and n[1] < self.grafo[parziale[-2]][parziale[-1]]["weight"]:    # cerco l'arco
                # con peso maggiore e continuo da quello
                parziale.append(n[0])
                self.ricorsione(parziale)
                parziale.pop()

    def get_score(self, nodes_list):
        score = 0
        for i in range(len(nodes_list)-1):
            score += self.grafo[nodes_list[i]][nodes_list[i+1]]["weight"]
        return score
