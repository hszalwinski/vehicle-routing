from typing import Callable, Any, List

from ortools.constraint_solver import pywrapcp

from algorithms.base import BaseSolver, SolverException


class OrtoolsSolver(BaseSolver):
    def __init__(self, distance_matrix_path: str, configuration_path: str, vehicles_path: str):
        super(OrtoolsSolver, self).__init__(distance_matrix_path, configuration_path, vehicles_path)
        self.distance_callback = self._create_distance_callback()
        self.depot = 0

    def _solve(self):
        routing = pywrapcp.RoutingModel(self.destinations_count, len(self.vehicles), self.depot)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        routing.SetArcCostEvaluatorOfAllVehicles(self.distance_callback)
        assignment = routing.SolveWithParameters(search_parameters)

        if not assignment:
            raise SolverException('No solution found.')

        best_sequnece = self._get_best_sequence(routing, assignment)
        best_sequence_cost = self._get_sequence_cost(best_sequnece)

        return best_sequnece, best_sequence_cost

    def _get_best_sequence(self, routing: Any, assignment: Any) -> List[int]:
        best_sequence = []

        index = routing.Start(self.depot)
        best_sequence.append(routing.IndexToNode(index))
        while not routing.IsEnd(index):
            index = assignment.Value(routing.NextVar(index))
            best_sequence.append(routing.IndexToNode(index))

        # Remove depot node
        best_sequence.pop(0)
        best_sequence.pop(-1)

        return best_sequence

    def _create_distance_callback(self) -> Callable:
        return self._arc_cost
