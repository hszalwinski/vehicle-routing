from typing import List, Tuple, Dict, Callable
from random import randint

from numpy import array, percentile
from plotly.offline import plot

from tools.charts.types import StatisticType, AggregatorType


class BaseChart:
    def __init__(self, statistic_type: str):
        self._statistic_type = StatisticType(statistic_type)
        self._chart_title = 'Default chart title'
        if self._statistic_type is StatisticType.COSTS:
            self._yaxis = {'title': 'Solution distance [m]'}
        elif self._statistic_type is StatisticType.EXECUTION_TIMES:
            self._yaxis = {'title': 'Time [s]'}
        else:
            raise Exception(f'Chart not implemented for: {statistic_type}')
        self._colors = ['rgb(255,0,0)', 'rgb(0,255,0)', 'rgb(0,0,255)', 'rgb(0,0,0)', 'rgb(255,0,255)']

    def _get_chart_data_from_csv_results(self, csv_results: List[dict]) -> Dict[int, Dict]:
        chart_data: Dict[int, Dict] = {}
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

    def _get_aggregation_method(self, aggregator: AggregatorType) -> Callable:
        if aggregator == AggregatorType.MIN:
            return lambda x: x.min()
        elif aggregator == AggregatorType.MEAN:
            return lambda x: x.mean()
        elif aggregator == AggregatorType.MAX:
            return lambda x: x.max()
        elif aggregator == AggregatorType.PERC90:
            return lambda x: percentile(x, 90)
        else:
            raise Exception(f'Unsupported aggregation method used: {aggregator}')

    def _get_data_to_plot(self, chart_data: Dict[int, Dict], aggregator: AggregatorType) \
            -> Tuple[List[int], List[float]]:
        aggregate = self._get_aggregation_method(aggregator)
        destinations_counts = []
        statistic_type_values = []
        for destinations_count, record in chart_data.items():
            destinations_counts.append(destinations_count)
            aggregated_statistic_type_values = aggregate(record[self._statistic_type.value])
            statistic_type_values.append(aggregated_statistic_type_values)

        return destinations_counts, statistic_type_values

    def _plot_chart(self, figure_data: List, filename: str):
        figure = {
            'data': figure_data,
            'layout': {
                'title': self._chart_title,
                'xaxis': {'title': 'Destinations count'},
                'yaxis': self._yaxis,
            }
        }
        plot(figure, filename=f'{filename}.html', image='jpeg', image_filename=filename)

    def _get_color(self, scatter_number):
        if scatter_number < len(self._colors):
            return self._colors[scatter_number]
        else:
            return f'rgb({randint(0, 255)},{randint(0, 255)},{randint(0, 255)})'
