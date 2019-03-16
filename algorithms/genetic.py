from random import sample, shuffle
from typing import List, Tuple

from algorithms.base import BaseSolver

ELITE_SELECTION_METHOD = 'elite'
TOURNAMENT_SELECTION_METHOD = 'tournament'
SELECTION_METHODS = (ELITE_SELECTION_METHOD, TOURNAMENT_SELECTION_METHOD)

PMX_CROSSING = 'pmx'
OTHER_CROSSING = 'other'
CROSSING_METHODS = (PMX_CROSSING, OTHER_CROSSING)


class GeneticSolver(BaseSolver):
    DEFAULT_ITERATIONS_COUNT = 1_000
    DEFAULT_POPULATION_SIZE = 100
    DEFAULT_SELECTION_METHOD = ELITE_SELECTION_METHOD
    DEFAULT_CROSSING_METHOD = PMX_CROSSING
    TOURNAMENT_GROUP_SIZE = 3

    def __init__(self, distance_matrix_path: str, configuration_path: str, vehicles_path: str,
                 population_size: int, iterations_count: int, selection_method: str, crossing_method: str):
        super(GeneticSolver, self).__init__(distance_matrix_path, configuration_path, vehicles_path)
        self._population_size = population_size
        self._iterations_count = iterations_count
        self._elite_count = 5
        self._perform_crossing = self._pmx_crossing if crossing_method == PMX_CROSSING else self._other_crossing
        self._groups_count = int(self._population_size / self.TOURNAMENT_GROUP_SIZE)

    def solve(self):
        population = self._generate_initial_population()
        population_with_costs = self._get_population_with_costs(population)

        for i in range(0, self._iterations_count):
            selected_sequences = self._perform_selection(population_with_costs)
            mutated_population = self._mutate_population(selected_sequences)

    def _generate_initial_population(self) -> List[List[int]]:
        basic_sequence = list(range(1, len(self.destinations)))
        population = [basic_sequence] * self._population_size

        for i in range(0, len(population)):
            population[i] = sample(population[i], k=len(self.destinations) - 1)

        return population

    def _get_population_with_costs(self, population: List[List[int]]) -> List[Tuple[float, List[int]]]:
        population_with_costs = []
        for sequence in population:
            population_with_costs.append(
                (self._get_sequence_cost(sequence), sequence)
            )

        return population_with_costs

    def _perform_selection(self, population_with_costs: List[Tuple[float, List[int]]]) -> List[List[int]]:
        selected_sequences = [] if self._elite_count == 0 else self._select_elites(population_with_costs)

        return self._tournament_selection(selected_sequences, population_with_costs)

    def _select_elites(self, population_with_costs: List[Tuple[float, List[int]]]) -> List[List[int]]:
        sorted_population = sorted(population_with_costs)
        elites = [sorted_population[i][1] for i in range(0, self._elite_count)]

        return elites

    def _tournament_selection(self, selected_sequences: List[List[int]],
                              population_with_costs: List[Tuple[float, List[int]]]) -> List[List[int]]:
        while True:
            shuffle(population_with_costs)
            tournament_groups = [population_with_costs[i::self._groups_count] for i in range(self._groups_count)]
            for group in tournament_groups:
                best_sequence_in_group = sorted(group)[0]
                selected_sequences.append(best_sequence_in_group)
                if len(selected_sequences) == self._population_size:
                    return selected_sequences

    def _mutate_population(self):
        pass
