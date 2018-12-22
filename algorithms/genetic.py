from random import sample
from collections import namedtuple

from algorithms.base import BaseSolver

RANK_REPRODUCE_METHOD = 'rank'
ROULETTE_REPRODUCE_METHOD = 'roulette'
REPRODUCE_METHODS = (RANK_REPRODUCE_METHOD, ROULETTE_REPRODUCE_METHOD)

Sequence = namedtuple('Sequence', ['list', 'cost'])


class GeneticSolver(BaseSolver):
    def __init__(self, distance_matrix_path, routes_to_find, population_size, iterations_count, reproduce_method):
        super(GeneticSolver, self).__init__(distance_matrix_path, routes_to_find)
        self._population_size = population_size
        self._iterations_count = iterations_count
        self._reproduce_population = self._rank_reproduce \
            if reproduce_method == RANK_REPRODUCE_METHOD else self._roulette_reproduce

    def solve(self):
        population = self._generate_initial_population()
        population_costs = self._get_population_costs(population)

        for i in range(0, self._iterations_count):
            self._reproduce_population(population, population_costs)

    def _generate_initial_population(self):
        # type: () -> list
        basic_sequence = list(range(1, len(self.destinations)))
        population = [basic_sequence] * self._population_size

        for i in range(0, len(population)):
            population[i] = sample(population[i], k=len(self.destinations) - 1)

        return population

    def _get_population_costs(self, population):
        # type: (list) -> list

        population_costs = []
        for sequence in population:
            population_costs.append(self._get_sequence_cost(sequence))

        return population_costs

    def _rank_reproduce(self, population, population_costs):
        # type: (list) -> list
        def get_cost(i):
            return population_costs[i]

        sorted_population = sorted(population, key=get_cost())

        pass

    def _roulette_reproduce(self, population, population_costs):
        # type: (list) -> list

        pass
