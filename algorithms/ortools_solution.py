from typing import Callable, Any

from ortools.constraint_solver import pywrapcp

from algorithms.base import BaseSolver


class OrtoolsSolver(BaseSolver):
    def __init__(self, distance_matrix_path: str, configuration_path: str, vehicles_path: str):
        super(OrtoolsSolver, self).__init__(distance_matrix_path, configuration_path, vehicles_path)
        self.distance_callback = self._create_distance_callback()
        self.depot = 0

    def solve(self):
        routing = pywrapcp.RoutingModel(self.destinations_count, len(self.vehicles), self.depot)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        routing.SetArcCostEvaluatorOfAllVehicles(self.distance_callback)
        assignment = routing.SolveWithParameters(search_parameters)
        self._print_results(routing, assignment)

    def _print_results(self, routing: Any, assignment: Any) -> None:
        if assignment:
            index = routing.Start(self.depot)
            route = ''
            while not routing.IsEnd(index):
                route += f'{index}  {self.destinations[routing.IndexToNode(index)]} \n'
                index = assignment.Value(routing.NextVar(index))
            route += str(self.destinations[routing.IndexToNode(index)])
            print("Route:\n" + route)
            print(f"\nTotal distance: {assignment.ObjectiveValue()} meters")
        else:
            print('No solution found.')

    def _create_distance_callback(self) -> Callable:
        return self._arc_cost
