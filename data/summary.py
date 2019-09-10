import os
from pathlib import Path

from tools.file_operations import load_csv_file

rows_count = 0
destinations_sum = 0
destinations_min = 99999999999999
destinations_max = 0
cost_sum = 0
cost_min = 999999999999999
cost_max = 0
execution_time_sum = 0
execution_time_min = 999999999999999
execution_time_max = 0

for path, subdirs, files in os.walk('./data/results'):
    for name in files:
        file_path = Path(path, name)
        headers, rows = load_csv_file(file_path)
        for row in rows:
            rows_count += 1

            destinations_count = int(row['destinations_count'])
            destinations_sum += destinations_count
            if destinations_count > destinations_max:
                destinations_max = destinations_count
            elif destinations_count < destinations_min:
                destinations_min = destinations_count

            cost = int(row['cost'])
            cost_sum += cost
            if cost > cost_max:
                cost_max = cost
            elif cost < cost_min:
                cost_min = cost

            execution_time = float(row['execution_time'])
            execution_time_sum += execution_time
            if execution_time > execution_time_max:
                execution_time_max = execution_time
            elif execution_time < execution_time_min:
                execution_time_min = execution_time

print(f'Rows count: {rows_count}')
print(f'Destinations min: {destinations_min}')
print(f'Destinations max: {destinations_max}')
print(f'Destinations sum: {destinations_sum}')
print(f'AVG destinations: {destinations_sum / rows_count}')
print(f'Cost min: {cost_min}')
print(f'Cost max: {cost_max}')
print(f'Cost sum: {cost_sum}')
print(f'AVG cost: {cost_sum / rows_count}')
print(f'Execution time sum: {execution_time_sum}')
print(f'Execution time min: {execution_time_min}')
print(f'Execution time max: {execution_time_max}')
print(f'AVG execution time: {execution_time_sum / rows_count}')
