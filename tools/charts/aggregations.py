from typing import Iterable

from plotly.graph_objs import Scatter

from tools.charts.base import BaseChart
from tools.charts.types import AggregatorType, DrawableStats, get_styles_for_aggregator
from tools.file_operations import load_csv_file


class AggregationChart(BaseChart):
    def build(self, drawable_stats: DrawableStats, aggregation_types: Iterable, filename: str):
        figure_data = []
        _, results = load_csv_file(drawable_stats.stats_path)
        chart_data = self._get_chart_data_from_csv_results(results)

        for at in aggregation_types:
            at = AggregatorType(at)
            at_styles = get_styles_for_aggregator(at)
            x, y = self._get_data_to_plot(chart_data, aggregator=at)
            figure_data.append(Scatter(x=x, y=y, name=at.value, **at_styles))

        self._chart_title = self._chart_title.format(algorithm=str(drawable_stats))
        self._plot_chart(figure_data, filename)
