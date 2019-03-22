from sys import maxsize as max_integer_size

from algorithms.base import BaseSolver

import itertools


class ScanAllSolver(BaseSolver):
    def __init__(self, distance_matrix_path: str, configuration_path: str, vehicles_path: str):
        super(ScanAllSolver, self).__init__(distance_matrix_path, configuration_path, vehicles_path)

    def _solve(self):
        destination_ids = range(1, self.destinations_count)
        permutations = itertools.permutations(destination_ids)

        best_sequence = None
        best_sequence_cost = max_integer_size
        for sequence in permutations:
            cost = self._get_sequence_cost(sequence)
            if cost < best_sequence_cost:
                best_sequence_cost = cost
                best_sequence = sequence

        return best_sequence, best_sequence_cost
