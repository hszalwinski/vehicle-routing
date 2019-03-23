from typing import Union
from pathlib import Path

from plotly.graph_objs import Scatter

from tools.chart.base import Aggregator, build_chart, get_chart_data_from_csv_results, get_costs_to_plot, \
    get_execution_time_to_plot

from tools.file_operations import load_csv_file


def build_cost_aggregation_chart(algorithm_name: str, csv_path: Union[str, Path], save_image: bool = False):
    figure_data = []
    _, results = load_csv_file(csv_path)
    chart_data = get_chart_data_from_csv_results(results)

    x, min_costs = get_costs_to_plot(chart_data, Aggregator.MIN)
    figure_data.append(Scatter(x=x, y=min_costs, name=Aggregator.MIN.value, line=dict(width=3, dash='dot')))

    x, mean_costs = get_costs_to_plot(chart_data, Aggregator.MEAN)
    figure_data.append(Scatter(x=x, y=mean_costs, mode='lines+markers', name=Aggregator.MEAN.value))

    x, max_costs = get_costs_to_plot(chart_data, Aggregator.MAX)
    figure_data.append(Scatter(x=x, y=max_costs, name=Aggregator.MAX.value, line=dict(width=3, dash='dot')))

    figure = {
        'data': figure_data,
        'layout': {
            'title': f'Odległość uzyskana przez algorytm "{algorithm_name}"',
            'xaxis': {'title': 'Ilość odwiedzonych miejsc'},
            'yaxis': {'title': 'Odległość [m]'},
        }
    }
    build_chart(figure, filename=f'{algorithm_name}_cost_aggregations', save_image=save_image)


def build_execution_time_aggregation_chart(algorithm_name: str, csv_path: Union[str, Path], save_image: bool = False):
    figure_data = []
    _, results = load_csv_file(csv_path)
    chart_data = get_chart_data_from_csv_results(results)

    x, min_execution_time = get_execution_time_to_plot(chart_data, Aggregator.MIN)
    figure_data.append(Scatter(x=x, y=min_execution_time, name=Aggregator.MIN.value, line=dict(width=3, dash='dot')))

    x, mean_execution_time = get_execution_time_to_plot(chart_data, Aggregator.MEAN)
    figure_data.append(Scatter(x=x, y=mean_execution_time, mode='lines+markers', name=Aggregator.MEAN.value))

    x, max_execution_time = get_execution_time_to_plot(chart_data, Aggregator.MAX)
    figure_data.append(Scatter(x=x, y=max_execution_time, name=Aggregator.MAX.value, line=dict(width=3, dash='dot')))

    figure = {
        'data': figure_data,
        'layout': {

            'title': f'Średni czas wykonania algorytmu "{algorithm_name}"',
            'xaxis': {'title': 'Ilość odwiedzonych miejsc'},
            'yaxis': {'title': 'Czas [s]'},
        }
    }
    build_chart(figure, filename=f'{algorithm_name}_execution_time_aggregations', save_image=save_image)
