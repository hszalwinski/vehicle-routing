from algorithms.base import BaseSolver
from timer import timer


class SimulatedAnnealingSolver(BaseSolver):
    def __init__(self, distance_matrix_path, routes_to_find=1):
        super(SimulatedAnnealingSolver, self).__init__(distance_matrix_path, routes_to_find)

    @timer
    def solve(self):
        pass
