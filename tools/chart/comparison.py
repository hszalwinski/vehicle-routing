from typing import Dict
from pathlib import Path

from plotly.graph_objs import Scatter

from tools.chart.base import Aggregator, get_chart_data_from_csv_results, get_costs_to_plot, get_execution_time_to_plot, \
    build_chart
from tools.file_operations import load_csv_file


def build_cost_comparison_chart(algorithms_data: Dict[str, Path or str], save_image=False):
    figure_data = []
    for name, path in algorithms_data.items():
        _, results = load_csv_file(path)
        chart_data = get_chart_data_from_csv_results(results)
        x, costs = get_costs_to_plot(chart_data, Aggregator.MEAN)
        figure_data.append(Scatter(x=x, y=costs, mode='lines+markers', name=name))

    figure = {
        'data': figure_data,
        'layout': {
            'title': 'Średnia odległość uzyskana przez algorytm',
            'xaxis': {'title': 'Ilość odwiedzonych miejsc'},
            'yaxis': {'title': 'Odległość [m]'},
        }
    }
    build_chart(figure, filename='algorithms_cost_comparison', save_image=save_image)


def build_execution_time_comparison_chart(algorithms_data: Dict[str, Path or str], save_image=False):
    figure_data = []
    for name, path in algorithms_data.items():
        _, results = load_csv_file(path)
        chart_data = get_chart_data_from_csv_results(results)
        x, costs = get_execution_time_to_plot(chart_data, Aggregator.MEAN)
        figure_data.append(Scatter(x=x, y=costs, mode='lines+markers', name=name))

    figure = {
        'data': figure_data,
        'layout': {
            'title': 'Średni czas wykonania algorytmu',
            'xaxis': {'title': 'Ilość odwiedzonych miejsc'},
            'yaxis': {'title': 'Czas [s]'},
        }
    }
    build_chart(figure, filename='algorithms_execution_time_comparison', save_image=save_image)
