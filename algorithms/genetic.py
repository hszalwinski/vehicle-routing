from random import sample, shuffle, randint
from typing import List, Tuple

from algorithms.base import BaseSolver


class GeneticSolver(BaseSolver):
    DEFAULT_ITERATIONS_COUNT = 1_000
    DEFAULT_POPULATION_SIZE = 100
    DEFAULT_ELITE_SEQUENCES_RATIO = 0.1
    DEFAULT_TOURNAMENT_GROUP_SIZE = 3
    DEFAULT_PMX_CROSSING_RATIO = 0.4
    DEFAULT_MUTATED_RATIO = 0.1

    def __init__(self, distance_matrix_path: str, configuration_path: str, vehicles_path: str,
                 population_size: int, iterations_count: int):
        super(GeneticSolver, self).__init__(distance_matrix_path, configuration_path, vehicles_path)
        self._population_size = population_size
        self._iterations_count = iterations_count
        self._elite_count = int(self.destinations_count * self.DEFAULT_ELITE_SEQUENCES_RATIO)
        if self._elite_count == 0:
            self._elite_count = 1
        self._groups_count = int(self._population_size / self.DEFAULT_TOURNAMENT_GROUP_SIZE)
        self._mutated_sequences_per_population = int(self._population_size * self.DEFAULT_MUTATED_RATIO)
        self._pmx_crossing_size = int(self.sequence_max_index * self.DEFAULT_PMX_CROSSING_RATIO)

        self._population = self._generate_initial_population()
        self._best_sequence = None
        self._best_sequence_cost = None

    def solve(self):
        for _ in range(0, self._iterations_count):
            population_with_costs = self._get_population_with_costs()
            elite_sequences, best_sequence_cost = self._select_elites(population_with_costs)
            if best_sequence_cost < self._best_sequence_cost:
                self._best_sequence = elite_sequences[0]
                self._best_sequence_cost = best_sequence_cost
            new_population = self._perform_selection(population_with_costs)
            population = self._perform_crossing(selected_population)
            population = self._mutate_population(crossed_population)

    def _generate_initial_population(self) -> List[List[int]]:
        basic_sequence = list(range(1, len(self.destinations)))
        population = [basic_sequence] * self._population_size

        for i in range(0, len(population)):
            population[i] = sample(population[i], k=len(self.destinations) - 1)

        return population

    def _get_population_with_costs(self) -> List[Tuple[float, List[int]]]:
        population_with_costs = []
        for sequence in self._population:
            population_with_costs.append(
                (self._get_sequence_cost(sequence), sequence)
            )

        return population_with_costs

    def _perform_selection(self, population_with_costs: List[Tuple[float, List[int]]]) -> List[List[int]]:

        return self._tournament_selection(selected_sequences, population_with_costs)

    def _select_elites(self, population_with_costs: List[Tuple[float, List[int]]]) -> List[List[int]]:
        sorted_population = sorted(population_with_costs)
        elites = [sorted_population[i][1] for i in range(0, self._elite_count)]
        best_sequence_cost = sorted_population[0][0]

        return elites, best_sequence_cost

    def _tournament_selection(self, selected_sequences: List[List[int]],
                              population_with_costs: List[Tuple[float, List[int]]]) -> List[List[int]]:
        while True:
            shuffle(population_with_costs)
            tournament_groups = [population_with_costs[i::self._groups_count] for i in range(self._groups_count)]
            for group in tournament_groups:
                best_sequence_in_group = sorted(group)[0]
                selected_sequences.append(best_sequence_in_group[1])
                if len(selected_sequences) == self._population_size:
                    return selected_sequences

    def _perform_crossing(self, population: List[List[int]]) -> List[List[int]]:
        shuffle(population)
        for i in range(0, len(population), 2):
            population[i], population[i + 1] = self._pmx_crossing(population[i], population[i + 1])

        return population

    def _pmx_crossing(self, sequence_a: List[int], sequence_b: List[int]) -> Tuple[List[int], List[int]]:
        start_index = randint(0, self.sequence_max_index - self._pmx_crossing_size)
        end_index = start_index + self._pmx_crossing_size
        sequence_a[start_index:end_index] = sequence_b[start_index:end_index]
        sequence_b[start_index:end_index] = sequence_a[start_index:end_index]

        return sequence_a, sequence_b

    def _mutate_population(self, population: List[List[int]]) -> List[List[int]]:
        sequence_ids_to_mutate = [
            randint(0, self._population_size) for _ in range(0, self._mutated_sequences_per_population)
        ]
        for sequence_id in sequence_ids_to_mutate:
            population[sequence_id] = self._mutate_by_inversion(population[sequence_id])

        return population

    def _mutate_by_inversion(self, sequence: List[int]) -> List[int]:
        index_a = randint(0, self.sequence_max_index)
        index_b = randint(0, self.sequence_max_index)

        if index_a <= index_b:
            sequence[index_a:index_b] = reversed(sequence[index_a:index_b])
        else:
            sequence[index_b:index_a] = reversed(sequence[index_b:index_a])

        return sequence
