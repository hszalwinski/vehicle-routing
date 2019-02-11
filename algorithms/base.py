import abc

from distance_matrix import DistanceMatrixManager


class BaseSolverException(Exception):
    pass


class BaseSolver(metaclass=abc.ABCMeta):
    def __init__(self, distance_matrix_path, routes_to_find):
        distance_matrix = DistanceMatrixManager.load_distance_matrix_from_pickle_file(path=distance_matrix_path)

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

    def _arc_cost(self, from_node, to_node):
        # type: (int, int) -> float

        return int(self.distance_matrix[from_node][to_node])

    def _get_sequence_cost(self, sequence):
        # type: (tuple or list) -> float

        sequence = self._update_sequence_with_depot_node(sequence)
        cost = 0
        for i in range(0, len(sequence) - 1):
            cost += self._arc_cost(sequence[i], sequence[i + 1])

        return cost

    def _print_results(self, sequence, cost):
        # type: (tuple or list, float) -> None

        sequence = self._update_sequence_with_depot_node(sequence)
        route = ''
        for index in sequence:
            route += f'{index}  {self.destinations[index]} \n'
        print("Route:\n" + route)
        print(f"Total distance: {cost} meters")

    @staticmethod
    def _update_sequence_with_depot_node(sequence):
        # type: (tuple or list) -> tuple or list

        if type(sequence) is tuple:
            sequence = (0,) + sequence + (0,)
        else:
            sequence = [0] + sequence + [0]

        return sequence
