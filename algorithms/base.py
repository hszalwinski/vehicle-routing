import abc

from distance_matrix import load_distance_matrix_from_pickle_file


class BaseSolverException(Exception):
    pass


class BaseSolver(metaclass=abc.ABCMeta):
    def __init__(self, distance_matrix_path, routes_to_find):
        distance_matrix = load_distance_matrix_from_pickle_file(path=distance_matrix_path)

        self.destinations = distance_matrix['destination_addresses']
        self.distance_matrix = distance_matrix['matrix']

        self.destinations_count = len(self.destinations)
        self.distance_matrix_size = len(self.distance_matrix)
        if (self.distance_matrix_size < 2) or (self.destinations_count < 2):
            raise BaseSolverException('Please provide at least 2 destinations in distance matrix.')

        self.routes_to_find = routes_to_find

    @abc.abstractmethod
    def solve(self):
        pass

    def arc_cost(self, from_node, to_node):
        return int(self.distance_matrix[from_node][to_node])
