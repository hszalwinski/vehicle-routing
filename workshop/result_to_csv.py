from pathlib import Path

from tools.file_operations import save_to_csv_file, load_from_json_file

json_path = Path('workshop/locations.json')
csv_path = Path('workshop/result.csv')

sequence = [0] + [6, 7, 5, 4, 2, 9, 1, 3, 8] + [0]
locations = load_from_json_file(json_path)

save_to_csv_file(csv_path, header=('latitude', 'longitude', 'name'), rows=[
    (locations[i]['latitude'], locations[i]['longitude'], locations[i]['name'])
    for i in sequence], delimiter=',')
