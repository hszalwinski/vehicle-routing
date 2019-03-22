from typing import Dict
from pathlib import Path

from plotly.graph_objs import Scatter

from tools.chart.base import Aggregator, get_chart_data_from_csv_results, get_costs_to_plot, get_execution_time_to_plot, \
    build_chart
from tools.file_operations import load_csv_file


def build_cost_aggregation_chart(algorithm_name: str, ], save_image=False):
    figure_data = []
    for name, path in algorithms_data:
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

line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4,
        dash = 'dot')