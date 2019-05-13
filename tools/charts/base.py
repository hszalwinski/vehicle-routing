from typing import List, Tuple, Dict, Callable

from numpy import array
from plotly.offline import plot

from tools.charts.types import StatisticType, AggregatorType


class BaseChart:
    def __init__(self, statistic_type: str):
        self._statistic_type = StatisticType(statistic_type)
        self._chart_title = 'Default chart title'
        if statistic_type is StatisticType.COST:
            self._yaxis = {'title': 'Solution distance [m]'}
        elif statistic_type is StatisticType.EXECUTION_TIME:
            self._yaxis = {'title': 'Time [s]'}
        else:
            raise Exception(f'Chart not implemented for: {statistic_type}')

    # noinspection PyTypeChecker
    def _get_chart_data_from_csv_results(self, csv_results: List[dict]) -> Dict[int, Dict]:
        chart_data = {}
        for result in csv_results:
            locations_count = int(result['locations_count'])
            if chart_data.get(locations_count) is None:
                chart_data[locations_count] = {'costs': [], 'execution_times': []}

            chart_data[locations_count]['costs'].append(float(result['cost']))
            chart_data[locations_count]['execution_times'].append(float(result['execution_time']))

        for record in chart_data.values():
            record['costs'] = array(record['costs'])
            record['execution_times'] = array(record['execution_times'])

        return chart_data

    def _get_aggregation_method(self, aggregator: AggregatorType) -> Callable:
        if aggregator == AggregatorType.MIN:
            return lambda x: x.min()
        elif aggregator == AggregatorType.MEAN:
            return lambda x: x.mean()
        elif aggregator == AggregatorType.MAX:
            return lambda x: x.max()
        else:
            raise Exception(f'Unsupported aggregation method used: {aggregator}')

    def _get_data_to_plot(self, chart_data: Dict[int, Dict], aggregator: AggregatorType) \
            -> Tuple[List[int], List[float]]:
        aggregate = self._get_aggregation_method(aggregator)
        locations_counts = []
        statistic_type_values = []
        for locations_count, record in chart_data.items():
            locations_counts.append(locations_count)
            aggregated_statistic_type_values = aggregate(record[self._statistic_type.value])
            statistic_type_values.append(aggregated_statistic_type_values)

        return locations_counts, statistic_type_values

    def _plot_chart(self, figure_data: List, filename: str):
        figure = {
            'data': figure_data,
            'layout': {
                'title': self._chart_title,
                'xaxis': {'title': 'Locations count'},
                'yaxis': self._yaxis,
            }
        }
        plot(figure, filename=f'{filename}.html', image='jpeg', image_filename=filename)
