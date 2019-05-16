from typing import List

from plotly.graph_objs import Scatter

from tools.charts.base import BaseChart
from tools.charts.types import AggregatorType, DrawableStats
from tools.file_operations import load_csv_file


class CustomChart(BaseChart):
    def __init__(self, statistic_type: str, aggregation_type=str, chart_tilte=str):
        super(CustomChart, self).__init__(statistic_type)
        self._chart_title = chart_tilte
        self._aggregation_type = AggregatorType(aggregation_type)

    def build(self, drawable_stats: List[DrawableStats], filename: str):
        figure_data = []
        for i, ds in enumerate(drawable_stats):
            _, results = load_csv_file(ds.stats_path)
            chart_data = self._get_chart_data_from_csv_results(results)
            x, y = self._get_data_to_plot(chart_data, self._aggregation_type)
            figure_data.append(Scatter(x=x, y=y, mode='lines+markers', name=str(ds),
                                       line=dict(color=self._get_color(i))))

        self._plot_chart(figure_data, filename)
