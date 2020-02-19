import json
from pathlib import Path

from tools.file_operations import load_csv_file

csv_path = Path('workshop/locations.csv')
json_path = Path('workshop/locations.json')

header, rows = load_csv_file(csv_path, delimiter=';')
i = 1
json_content = []
for row in rows:
    json_content.append({
        'locationId': i,
        'latitude': float(row['latitude']),
        'longitude': float(row['longitude']),
        'name': row['name']
    })
    i += 1

json_path.write_text(json.dumps(json_content))
