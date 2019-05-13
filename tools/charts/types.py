from enum import Enum
from pathlib import Path


class StatisticType(Enum):
    COST = 'cost'
    EXECUTION_TIME = 'execution_time'


class AggregatorType(Enum):
    MIN = 'min'
    MEAN = 'mean'
    MAX = 'max'


def get_styles_for_aggregator(aggregator: AggregatorType) -> dict:
    if aggregator in (AggregatorType.MIN, AggregatorType.MAX):
        return dict(line=dict(width=3, dash='dot'))
    else:
        return dict(mode='lines+markers')


STATISTIC_TYPES = [t.value for t in list(StatisticType)]
AGGREGATOR_TYPES = [t.value for t in list(AggregatorType)]


class DrawableStats:
    NAME = 'Name to display'

    def __init__(self, stats_path):
        self.stats_path = Path(stats_path)

    def __str__(self):
        return self.NAME


class ScanAllDrawableStats(DrawableStats):
    NAME = 'Scan all'


class ORToolsDrawableStats(DrawableStats):
    NAME = 'OR-Tools'


class GeneticDrawableStats(DrawableStats):
    NAME = 'Genetic algorithm'


class SimulatedAnnealingDrawableStats(DrawableStats):
    NAME = 'Simulated annealing'