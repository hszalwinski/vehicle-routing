from subprocess import run

import click

from algorithms.genetic import GeneticSolver
from algorithms.ortools_solution import OrtoolsSolver
from algorithms.scan_all import ScanAllSolver
from algorithms.simulated_annealing import SimulatedAnnealingSolver
from tools.charts.aggregations import AggregationChart
from tools.charts.comparison import ComparisonChart
from tools.charts.custom import CustomChart
from tools.charts.types import STATISTIC_TYPES, AGGREGATOR_TYPES, ScanAllDrawableStats, ORToolsDrawableStats, \
    GeneticDrawableStats, SimulatedAnnealingDrawableStats, AggregatorType, CustomDrawableStats
from tools.distance_matrix import DistanceMatrixManager

SCAN_ALL = 'scan-all'
ORTOOLS = 'ortools'
GENETIC = 'genetic'
SIMULATED_ANNEALING = 'simulated-annealing'
ALGORITHM_COMMANDS = (SCAN_ALL, ORTOOLS, GENETIC, SIMULATED_ANNEALING)


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
@click.option('--distance-matrix', '-d', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--configuration', '-c', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--vehicles', '-v', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--output-file', '-o', type=click.Path(writable=True, resolve_path=True), required=False)
def scan_all(distance_matrix, configuration, vehicles, output_file):
    """
    Solves VRP scanning all results.
    """
    ScanAllSolver(distance_matrix, configuration, vehicles, output_file).solve()


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--configuration', '-c', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--vehicles', '-v', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--output-file', '-o', type=click.Path(writable=True, resolve_path=True), required=False)
def ortools(distance_matrix, configuration, vehicles, output_file):
    """
    Solves VRP using Google ORTools algorithms.
    """
    OrtoolsSolver(distance_matrix, configuration, vehicles, output_file).solve()


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--configuration', '-c', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--vehicles', '-v', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--output-file', '-o', type=click.Path(writable=True, resolve_path=True), required=False)
def simulated_annealing(distance_matrix, configuration, vehicles, output_file):
    """
    Solves VRP using simulated annealing.
    """
    SimulatedAnnealingSolver(distance_matrix, configuration, vehicles, output_file).solve()


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--configuration', '-c', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--vehicles', '-v', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--output-file', '-o', type=click.Path(writable=True, resolve_path=True), required=False)
def genetic(distance_matrix, configuration, vehicles, output_file):
    """
    Solves VRP using genetic algorithm.
    """
    GeneticSolver(distance_matrix, configuration, vehicles, output_file).solve()


@cli.command()
@click.option('--algorithm', '-al', type=click.Choice(ALGORITHM_COMMANDS), required=True)
@click.option('--iterations', '-i', type=click.IntRange(1, 1_000_000), required=False, default=1)
@click.option('--distance-matrix', '-d', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--configuration', '-c', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--vehicles', '-v', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--output-file', '-o', type=click.Path(writable=True, resolve_path=True), required=False)
def simulation(algorithm, iterations, distance_matrix, configuration, vehicles, output_file):
    """
    'iterations' times solves a VRP using chosen algorithm.
    """
    for _ in range(0, iterations):
        run(['python', 'vrp.py', algorithm,
             '-d', distance_matrix,
             '-c', configuration,
             '-v', vehicles,
             '-o', output_file])


@cli.command()
@click.option('--chart-title', '-ct', type=click.STRING, required=True)
@click.option('--statistic-type', '-st', type=click.Choice(STATISTIC_TYPES), required=True)
@click.option('--output-filename', '-of', type=click.STRING, required=True)
@click.option('--aggregation-type', '-at', type=click.Choice(AGGREGATOR_TYPES), required=False,
              default=AggregatorType.MEAN)
@click.option('--scan-all', '-sca', type=click.Path(exists=True, resolve_path=True), required=False)
@click.option('--ortools', '-or', type=click.Path(exists=True, resolve_path=True), required=False)
@click.option('--genetic', '-g', type=click.Path(exists=True, resolve_path=True), required=False)
@click.option('--simulated-annealing', '-sia', type=click.Path(exists=True, resolve_path=True), required=False)
def comparison_chart(chart_title, statistic_type, output_filename, aggregation_type,
                     scan_all=None, ortools=None, genetic=None, simulated_annealing=None):
    """
    Compares different algorithms results.
    """
    drawable_stats = []
    if scan_all:
        drawable_stats.append(ScanAllDrawableStats(scan_all))
    if ortools:
        drawable_stats.append(ORToolsDrawableStats(ortools))
    if genetic:
        drawable_stats.append(GeneticDrawableStats(genetic))
    if simulated_annealing:
        drawable_stats.append(SimulatedAnnealingDrawableStats(simulated_annealing))

    if drawable_stats:
        chart = ComparisonChart(statistic_type, chart_title)
        chart.build(drawable_stats, output_filename, aggregation_type)


@cli.command()
@click.option('--chart-title', '-ct', type=click.STRING, required=True)
@click.option('--statistic-type', '-st', type=click.Choice(STATISTIC_TYPES), required=True)
@click.option('--algorithm', '-al', type=click.Choice(ALGORITHM_COMMANDS), required=True)
@click.option('--input-file', '-if', type=click.Path(exists=True, resolve_path=True), required=True)
@click.option('--aggregation-type', '-at', type=click.Choice(AGGREGATOR_TYPES), required=True, multiple=True)
@click.option('--output-filename', '-of', type=click.STRING, required=True)
def aggregation_chart(chart_title, statistic_type, algorithm, input_file, aggregation_type, output_filename):
    """
    Combines multiple result aggregations for a single algorithm. Multiple 'aggregation-type'
    parameters can be provided.
    """
    if algorithm == SCAN_ALL:
        drawable_stats = ScanAllDrawableStats(input_file)
    elif algorithm == ORTOOLS:
        drawable_stats = ORToolsDrawableStats(input_file)
    elif algorithm == GENETIC:
        drawable_stats = GeneticDrawableStats(input_file)
    elif algorithm == SIMULATED_ANNEALING:
        drawable_stats = SimulatedAnnealingDrawableStats(input_file)
    else:
        raise Exception('Implementation error')

    chart = AggregationChart(statistic_type, chart_title)
    chart.build(drawable_stats, aggregation_type, output_filename)


@cli.command()
@click.option('--chart-title', '-ct', type=click.STRING, required=True)
@click.option('--statistic-type', '-st', type=click.Choice(STATISTIC_TYPES), required=True)
@click.option('--output-filename', '-of', type=click.STRING, required=True)
@click.option('--aggregation-type', '-at', type=click.Choice(AGGREGATOR_TYPES), required=False,
              default=AggregatorType.MEAN)
@click.option('--input-file', '-if', type=click.Path(exists=True, resolve_path=True), required=False, multiple=True)
def custom_chart(chart_title, statistic_type, output_filename, aggregation_type, input_file):
    """
    Compares custom results. Multiple 'input_file' parameters can be provided.
    """
    drawable_stats = [CustomDrawableStats(i) for i in input_file]
    chart = CustomChart(statistic_type, aggregation_type, chart_title)
    chart.build(drawable_stats, output_filename)


if __name__ == '__main__':
    cli()
