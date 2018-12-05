import sys

from algorithms.base import BaseSolver
from timer import timer

import itertools


class ScanAllSolver(BaseSolver):
    def __init__(self, distance_matrix_path, routes_to_find=1):
        super(ScanAllSolver, self).__init__(distance_matrix_path, routes_to_find)

    @timer
    def solve(self):
        destination_ids = range(1, self.destinations_count)
        permutations = itertools.permutations(destination_ids)

        min_sequence = None
        min_cost = sys.maxsize
        for sequence in permutations:
            sequence = (0,) + sequence + (0,)
            cost = self._get_sequence_cost(sequence)
            if cost < min_cost:
                min_cost = cost
                min_sequence = sequence

        self._print_results(min_sequence, min_cost)

    def _get_sequence_cost(self, sequence):
        cost = 0
        for i in range(0, len(sequence) - 1):
            cost += self.arc_cost(sequence[i], sequence[i + 1])

        return cost

    def _print_results(self, min_sequence, min_cost):
        route = ''
        for index in min_sequence:
            route += f'{index}  {self.destinations[index]} \n'
        print("Route:\n" + route)
        print(f"Total distance: {min_cost} meters")
