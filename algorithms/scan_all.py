import sys

from algorithms.base import BaseSolver

import itertools


class ScanAllSolver(BaseSolver):
    def __init__(self, distance_matrix_path: str, configuration_path: str, vehicles_path: str):
        super(ScanAllSolver, self).__init__(distance_matrix_path, configuration_path, vehicles_path)

    def solve(self):
        destination_ids = range(1, self.destinations_count)
        permutations = itertools.permutations(destination_ids)

        solution = None
        solution_cost = sys.maxsize
        for sequence in permutations:
            cost = self._get_sequence_cost(sequence)
            if cost < solution_cost:
                solution_cost = cost
                solution = sequence

        self._print_results(solution, solution_cost)
