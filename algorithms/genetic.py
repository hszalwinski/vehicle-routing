from random import sample

from algorithms.base import BaseSolver

RANK_SELECTION_METHOD = 'rank'
ROULETTE_SELECTION_METHOD = 'roulette'
SELECTION_METHODS = (RANK_SELECTION_METHOD, ROULETTE_SELECTION_METHOD)

PMX_CROSSING = 'pmx'
CROSSING_METHODS = (PMX_CROSSING,)


class GeneticSolver(BaseSolver):
    DEFAULT_ITERATIONS_COUNT = 1_000
    DEFAULT_POPULATION_SIZE = 100
    DEFAULT_SELECTION_METHOD = RANK_SELECTION_METHOD
    DEFAULT_CROSSING_METHOD = PMX_CROSSING

    def __init__(self, distance_matrix_path, configuration, vehicles, population_size, iterations_count,
                 selection_method):
        super(GeneticSolver, self).__init__(distance_matrix_path, configuration, vehicles)
        self._population_size = population_size
        self._iterations_count = iterations_count
        self._perform_selection = self._rank_selection if selection_method == RANK_SELECTION_METHOD \
            else self._roulette_selection
        self._perform_crossing = self._pmx_crossing

    def solve(self):
        population = self._generate_initial_population()
        population_costs = self._get_population_costs(population)

        for i in range(0, self._iterations_count):
            population_with_costs = zip(population, population_costs)
            selected_sequences = self._perform_selection(population_with_costs)

    def _generate_initial_population(self) -> list:
        basic_sequence = list(range(1, len(self.destinations)))
        population = [basic_sequence] * self._population_size

        for i in range(0, len(population)):
            population[i] = sample(population[i], k=len(self.destinations) - 1)

        return population

    def _get_population_costs(self, population: list) -> list:
        population_costs = []
        for sequence in population:
            population_costs.append(self._get_sequence_cost(sequence))

        return population_costs

    def _rank_selection(self, population_with_costs: list) -> list:
        def get_cost(sequence):
            return sequence[1]

        population_with_costs = sorted(population_with_costs, key=get_cost)
        sorted_population, _ = zip(*population_with_costs)
        slice_stop = int(self._population_size / 2)
        selected_sequences = list(sorted_population[:slice_stop])

        return selected_sequences

    @staticmethod
    def _roulette_selection(population: list, population_costs: list) -> list:
        pass

    def _pmx_crossing(self):
        pass
