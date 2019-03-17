import numpy as np

from typing import List
from random import shuffle, random, randint
from copy import deepcopy

from algorithms.base import BaseSolver


class SimulatedAnnealingSolver(BaseSolver):
    DEFAULT_TEMPERATURE_FACTOR = 100
    DEFAULT_ITERATIONS_COUNT = 1_000

    def __init__(self, distance_matrix_path: str, configuration_path: str, vehicles_path: str,
                 iterations_count: int, temperature_factor: int):
        super(SimulatedAnnealingSolver, self).__init__(distance_matrix_path, configuration_path, vehicles_path)
        self._temperature_factor = temperature_factor
        self._iterations_count = iterations_count

        self._best_sequence = self._generate_initial_sequence()
        self._best_sequence_cost = self._get_sequence_cost(self._best_sequence)

    def solve(self):
        sequence = deepcopy(self._best_sequence)

        for i in range(0, self._iterations_count):
            new_sequence = self._create_new_sequence(deepcopy(sequence))
            cost = self._get_sequence_cost(new_sequence)

            if cost < self._best_sequence_cost:
                sequence = new_sequence
                self._best_sequence = deepcopy(sequence)
                self._best_sequence_cost = deepcopy(cost)
                # print(f"New solution: {self._solution} cost: {self._solution_cost}")
            else:
                if self.calculate_probability(i, cost) > random():
                    sequence = new_sequence

        self._print_results(self._best_sequence, self._best_sequence_cost)

    def _generate_initial_sequence(self) -> List[int]:
        init_sequence = list(range(1, len(self.destinations)))
        shuffle(init_sequence)

        return init_sequence

    def _create_new_sequence(self, sequence: List[int]) -> List[int]:
        """
        Changes 2 points place in a sequence
        """
        index_a = randint(0, self.sequence_max_index)
        index_b = randint(0, self.sequence_max_index)

        if index_a != index_b:
            sequence[index_a], sequence[index_b] = sequence[index_b], sequence[index_a]
        else:
            self._create_new_sequence(sequence)

        return sequence

    def calculate_probability(self, iteration_number: int, cost: float) -> float:
        temperature = self._calculate_temperature(iteration_number)
        probability = np.power(np.e, -1 * (cost - self._best_sequence_cost) / temperature)

        return probability

    def _calculate_temperature(self, iteration_number: int) -> float:
        return self._temperature_factor / np.log(iteration_number + 1)
