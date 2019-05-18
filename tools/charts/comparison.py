from typing import List

from plotly.graph_objs import Scatter

from tools.charts.base import BaseChart
from tools.charts.types import AggregatorType, DrawableStats
from tools.file_operations import load_csv_file


class ComparisonChart(BaseChart):
    def build(self, drawable_stats: List[DrawableStats], filename: str, aggregation_type: str):
        aggregation_type = AggregatorType(aggregation_type)
        figure_data = []
        for ds in drawable_stats:
            _, results = load_csv_file(ds.stats_path)
            chart_data = self._get_chart_data_from_csv_results(results)
            x, y = self._get_data_to_plot(chart_data, aggregation_type)
            figure_data.append(Scatter(x=x, y=y, mode='lines+markers', name=str(ds)))

        self._plot_chart(figure_data, filename)
