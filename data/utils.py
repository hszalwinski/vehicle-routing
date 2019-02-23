from json import dumps, loads
from pathlib import Path


def get_new_data_dict():
    return {
        'configuration': {
            'optimization': {
                'minimizeWaitingTime': False,
                'minimizeVehiclesUsed': False
            },
            'constraints': {
                'maxWorkTimeEnabled': True,
                'maxRouteDistanceEnabled': True,
                'maxRouteTimeEnabled': True
            }
        },
        'vehicles': [
            {
                'vehicleId': 1,
                'maxWorkTime': 600,
                'maxRouteDistance': 400,
                'totalCapacity': 17300
            },
            {
                'vehicleId': 2,
                'maxWorkTime': 600,
                'maxRouteDistance': 400,
                'totalCapacity': 17661
            }
        ],
        'locations': []
    }


def create_new_format_json(old_format_file_path: Path, new_format_file_path: Path) -> None:
    data_dict = loads(old_format_file_path.read_bytes())
    new_data_dict = get_new_data_dict()

    i = 1
    for route_task in data_dict.get('normalRouteTasks'):
        location = {
            'locationId': i,
            'latitude': route_task['latitude'],
            'longitude': route_task['longitude']
        }
        new_data_dict['locations'].append(location)
        i += 1

    new_format_file_path.write_text(dumps(new_data_dict))


def create_n_locations_example_json(all_data_dict: dict, n: int) -> None:
    new_data_dict = get_new_data_dict()
    new_data_dict['locations'] = all_data_dict['locations'][:n]
    Path('data', 'input', f'e{n}.json').write_text(dumps(new_data_dict))


if __name__ == '__main__':
    all_data_dict = loads(Path('data', 'input', 'all.json').read_bytes())

    min_locations = 3
    for n in range(min_locations, 31):
        create_n_locations_example_json(all_data_dict, n)
