from enum import Enum
from pathlib import Path
from typing import List, Tuple, Dict, Callable

from numpy import array

from plotly.offline import plot

RESULTS_DIR = Path('data', 'results')


class Aggregator(Enum):
    MIN = 'min'
    MEAN = 'mean'
    MAX = 'max'


def get_aggregation_method(aggregator: Aggregator) -> Callable:
    if aggregator == Aggregator.MIN:
        return lambda x: x.min()
    elif aggregator == Aggregator.MEAN:
        return lambda x: x.mean()
    elif aggregator == Aggregator.MAX:
        return lambda x: x.max()
    else:
        raise Exception(f'Unsupported aggregation method used: {aggregator}')


# noinspection PyTypeChecker
def get_chart_data_from_csv_results(csv_results: List[dict]) -> Dict[int, Dict]:
    chart_data = {}
    for result in csv_results:
        destinations_count = int(result['destinations_count'])
        if chart_data.get(destinations_count) is None:
            chart_data[destinations_count] = {'costs': [], 'execution_times': []}

        chart_data[destinations_count]['costs'].append(float(result['cost']))
        chart_data[destinations_count]['execution_times'].append(float(result['execution_time']))

    for record in chart_data.values():
        record['costs'] = array(record['costs'])
        record['execution_times'] = array(record['execution_times'])

    return chart_data


def get_costs_to_plot(chart_data: Dict[int, Dict], aggregator: Aggregator) -> Tuple[List[int], List[float]]:
    aggregate = get_aggregation_method(aggregator)
    destinations_counts = []
    costs = []
    for destinations_count, record in chart_data.items():
        destinations_counts.append(destinations_count)
        costs.append(aggregate(record['costs']))

    return destinations_counts, costs


def get_execution_time_to_plot(chart_data: Dict[int, Dict], aggregator: Aggregator) -> Tuple[List[int], List[float]]:
    aggregate = get_aggregation_method(aggregator)
    destinations_counts = []
    execution_times = []
    for destinations_count, record in chart_data.items():
        destinations_counts.append(destinations_count)
        execution_times.append(aggregate(record['execution_times']))

    return destinations_counts, execution_times


def build_chart(figure, filename, save_image=False):
    if save_image:
        plot(figure, filename=f'{filename}.html', image='jpeg', image_filename=filename)
    else:
        plot(figure, filename=f'{filename}.html')
