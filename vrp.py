import click
from subprocess import run

from algorithms.genetic import GeneticSolver
from algorithms.scan_all import ScanAllSolver
from algorithms.simulated_annealing import SimulatedAnnealingSolver
from algorithms.ortools_solution import OrtoolsSolver
from tools.distance_matrix import DistanceMatrixManager


@click.group()
def cli():
    """
    This CLI is an entrypoint for utilities and all simulations used to analyze
    different vehicle routing problem solutions.
    """


@cli.command()
@click.option('--app-key', '-a', envvar='APP_KEY', type=click.STRING, required=True)
@click.option('--locations-json', '-i', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--output-csv', '-oc', type=click.Path(writable=True, resolve_path=True), required=True)
@click.option('--output-pickle', '-op', type=click.Path(writable=True, resolve_path=True))
def distance_matrix(app_key, locations_json, output_csv, output_pickle):
    """
    Creates distance matrix files (CSV, pickle) from input JSONs using Google Distance Matrix API.
    """
    DistanceMatrixManager(app_key).create_distance_matrix(locations_json, output_csv, output_pickle)


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(), required=True)
@click.option('--configuration', '-c', type=click.Path(), required=True)
@click.option('--vehicles', '-v', type=click.Path(), required=True)
@click.option('--output-file', '-o', type=click.Path(writable=True, resolve_path=True), required=False)
def scan_all(distance_matrix, configuration, vehicles, output_file):
    """
    Solves VRP scanning all results.
    """
    ScanAllSolver(distance_matrix, configuration, vehicles, output_file).solve()


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(), required=True)
@click.option('--configuration', '-c', type=click.Path(), required=True)
@click.option('--vehicles', '-v', type=click.Path(), required=True)
@click.option('--output-file', '-o', type=click.Path(writable=True, resolve_path=True), required=False)
def ortools(distance_matrix, configuration, vehicles, output_file):
    """
    Solves VRP using Google ORTools algorithms.
    """
    OrtoolsSolver(distance_matrix, configuration, vehicles, output_file).solve()


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(), required=True)
@click.option('--configuration', '-c', type=click.Path(), required=True)
@click.option('--vehicles', '-v', type=click.Path(), required=True)
@click.option('--output-file', '-o', type=click.Path(writable=True, resolve_path=True), required=False)
def simulated_annealing(distance_matrix, configuration, vehicles, output_file):
    """
    Solves VRP using simulated annealing.
    """
    SimulatedAnnealingSolver(distance_matrix, configuration, vehicles, output_file).solve()


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(), required=True)
@click.option('--configuration', '-c', type=click.Path(), required=True)
@click.option('--vehicles', '-v', type=click.Path(), required=True)
@click.option('--output-file', '-o', type=click.Path(writable=True, resolve_path=True), required=False)
def genetic(distance_matrix, configuration, vehicles, output_file):
    """
    Solves VRP using genetic algorithm.
    """
    GeneticSolver(distance_matrix, configuration, vehicles, output_file).solve()


@cli.command()
@click.option('--algorithm', '-al', type=click.Choice(['scan_all', 'ortools', 'simulated_annealing', 'genetic']),
              required=True)
@click.option('--distance-matrix', '-d', type=click.Path(), required=True)
@click.option('--configuration', '-c', type=click.Path(), required=True)
@click.option('--vehicles', '-v', type=click.Path(), required=True)
@click.option('--output-file', '-o', type=click.Path(writable=True, resolve_path=True), required=False)
def simulation(algorithm, distance_matrix, configuration, vehicles, output_file):
    for destinations_count in range(4, 31):
        for iteration_number in range(0, 10):
            run(['python', 'vrp.py', algorithm,
                 '-d', distance_matrix,
                 '-c', configuration,
                 '-v', vehicles,
                 '-o', output_file])


if __name__ == '__main__':
    cli()
