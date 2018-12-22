import numpy as np

from random import shuffle, random, randint
from copy import deepcopy

from algorithms.base import BaseSolver

DEFAULT_TEMPERATURE_FACTOR = 100


class SimulatedAnnealingSolver(BaseSolver):
    def __init__(self, distance_matrix_path, routes_to_find, temperature_factor, iterations_count):
        super(SimulatedAnnealingSolver, self).__init__(distance_matrix_path, routes_to_find)
        self._solution = self._generate_initial_sequence()
        self._solution_cost = self._get_sequence_cost(self._solution)
        self._temperature_factor = temperature_factor
        self._iterations_count = iterations_count

    def solve(self):
        sequence = deepcopy(self._solution)

        for i in range(0, self._iterations_count):
            new_sequence = self._create_new_sequence(deepcopy(sequence))
            cost = self._get_sequence_cost(new_sequence)

            if cost < self._solution_cost:
                sequence = new_sequence
                self._solution = deepcopy(sequence)
                self._solution_cost = deepcopy(cost)
                # print(f"New solution: {self._solution} cost: {self._solution_cost}")
            else:
                if self.calculate_probability(i, cost) > random():
                    sequence = new_sequence

        self._print_results(self._solution, self._solution_cost)

    def _generate_initial_sequence(self):
        # type: () -> list

        init_sequence = list(range(1, len(self.destinations)))
        shuffle(init_sequence)

        return init_sequence

    def _create_new_sequence(self, sequence):
        # type: (list) -> list
        '''
        Change places in sequence of 2 points
        '''
        index_a = randint(0, len(sequence) - 1)
        index_b = randint(0, len(sequence) - 1)

        if index_a != index_b:
            sequence[index_a], sequence[index_b] = sequence[index_b], sequence[index_a]
        else:
            self._create_new_sequence(sequence)

        return sequence

    def calculate_probability(self, iteration_number, cost):
        # type: (int, float) -> float

        temperature = self._calculate_temperature(iteration_number)
        probability = np.power(np.e, -1 * (cost - self._solution_cost) / temperature)

        return probability

    def _calculate_temperature(self, iteration_number):
        # type: (int) -> float

        return self._temperature_factor / np.log(iteration_number + 1)
