from model.model import Model

my_model = Model()
my_model.get_years()
year = 2015
my_model.get_teams_of_year(year)
my_model.build_graph()
my_model.print_graph_details()