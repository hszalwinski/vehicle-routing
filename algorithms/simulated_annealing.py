from algorithms.base import BaseSolver


class SimulatedAnnealingSolver(BaseSolver):
    def __init__(self, distance_matrix_path, depot=0, routes_to_find=1):
        super(SimulatedAnnealingSolver, self).__init__(distance_matrix_path, depot, routes_to_find)

    def solve(self):
        pass
