import os
from pathlib import Path

from tools.file_operations import load_csv_file

rows_count = 0
destinations_sum = 0
cost_sum = 0
execution_time_sum = 0

for path, subdirs, files in os.walk('./data/results'):
    for name in files:
        file_path = Path(path, name)
        headers, rows = load_csv_file(file_path)
        for row in rows:
            rows_count += 1
            destinations_sum += int(row['destinations_count'])
            cost_sum += int(row['cost'])
            execution_time_sum += float(row['execution_time'])

print(f'Rows count: {rows_count}')
print(f'Destinations sum: {destinations_sum}')
print(f'AVG destinations: {destinations_sum / rows_count}')
print(f'Cost: {cost_sum}')
print(f'AVG cost: {cost_sum / rows_count}')
print(f'Execution time sum: {execution_time_sum}')
print(f'AVG execution time: {execution_time_sum / rows_count}')
