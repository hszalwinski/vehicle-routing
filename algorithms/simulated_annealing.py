import numpy as np

from timer import timer
from random import shuffle, random, randint

from algorithms.base import BaseSolver

DEFAULT_ANNEALING_SPEED = 10
DEFAULT_ITERATIONS_COUNT = 1000


class SimulatedAnnealingSolver(BaseSolver):
    def __init__(self, distance_matrix_path, routes_to_find, annealing_speed, iterations_count):
        super(SimulatedAnnealingSolver, self).__init__(distance_matrix_path, routes_to_find)
        self._solution = self._generate_initial_sequence()
        self._solution_cost = self._get_sequence_cost(self._solution)
        self._annealing_speed = annealing_speed
        self._iterations_count = iterations_count

    @timer
    def solve(self):
        sequence = self._solution

        for i in range(0, self._iterations_count):
            new_sequence = self._create_new_sequence(sequence)
            cost = self._get_sequence_cost(new_sequence)

            if cost < self._solution_cost:
                self._solution = new_sequence
                self._solution_cost = cost
            else:
                if random() > self.calculate_probability(i, cost):
                    pass

    def _generate_initial_sequence(self):
        # type: () -> list

        init_sequence = list(range(1, len(self.destinations)))
        shuffle(init_sequence)

        return init_sequence

    def _create_new_sequence(self, sequence):
        # type: (list) -> list

        index1 = randint(0, len(sequence))
        next1 = index1 + 1 if index1 + 1 <
        random_index2 = randint(0, len(sequence))



        return sequence

    def calculate_probability(self, iteration_number, cost):
        # type: (int, float) -> float

        temperature = self._calculate_temperature(iteration_number)
        probability = np.power(np.e, -1 * (cost - self._solution_cost) / temperature)

        return probability

    def _calculate_temperature(self, interation_number):
        # type: (int) -> float

        T = self._annealing_speed / np.log10(interation_number + 10)

        return T
