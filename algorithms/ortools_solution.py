from ortools.constraint_solver import pywrapcp

from algorithms.base import BaseSolver
from timer import timer


class OrtoolsSolver(BaseSolver):
    def __init__(self, distance_matrix_path, depot, routes_to_find):
        super(OrtoolsSolver, self).__init__(distance_matrix_path, depot, routes_to_find)
        self.distance_callback = self._create_distance_callback()

    @timer
    def solve(self):
        routing = pywrapcp.RoutingModel(self.destinations_count, self.routes_to_find, self.depot)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        routing.SetArcCostEvaluatorOfAllVehicles(self.distance_callback)
        assignment = routing.SolveWithParameters(search_parameters)
        self._print_results(routing, assignment)

    def _print_results(self, routing, assignment):
        if assignment:
            route_number = 0
            index = routing.Start(route_number)
            route = ''
            while not routing.IsEnd(index):
                route += str(index) + '  ' + str(self.destinations[routing.IndexToNode(index)]) + ' -> \n'
                index = assignment.Value(routing.NextVar(index))
            route += str(self.destinations[routing.IndexToNode(index)])
            print("Route:\n" + route)
            print("\nTotal distance: " + str(assignment.ObjectiveValue()) + " meters")
        else:
            print('No solution found.')

    def _create_distance_callback(self):
        # type: () -> function

        def distance_callback(from_node, to_node):
            return int(self.distance_matrix[from_node][to_node])

        return distance_callback
