from pathlib import Path

from tools.chart.base import RESULTS_DIR

# Set working directory to project root directory
from tools.chart.comparison import build_cost_comparison_chart, build_execution_time_comparison_chart

SCAN_ALL_NAME = 'Sprawdź wszystkie'
SCAN_ALL_PATH = Path(RESULTS_DIR, 'tsp-scan_all-01.csv')

ORTOOLS_NAME = 'OR Tools'
ORTOOLS_PATH = Path(RESULTS_DIR, 'tsp-ortools-01.csv')

GENETIC_NAME = 'Genetyczny'
GENETIC_PATH = Path(RESULTS_DIR, 'tsp-genetic-01.csv')

SIMULATED_ANNEALING_NAME = 'Symulowane wyżarzanie'
SIMULATED_ANNEALING_PATH = Path(RESULTS_DIR, 'tsp-simulated_annealing-01.csv')

algorithms_data = {
    SCAN_ALL_NAME: SCAN_ALL_PATH,
    ORTOOLS_NAME: ORTOOLS_PATH,
    GENETIC_NAME: GENETIC_PATH,
    SIMULATED_ANNEALING_NAME: SIMULATED_ANNEALING_PATH
}

build_cost_comparison_chart(algorithms_data)
build_execution_time_comparison_chart(algorithms_data)
build_cost_aggregation_chart()