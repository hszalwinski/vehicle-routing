from subprocess import run

# Set working directory to project root directory

for destinations_count in range(4, 31):
    for iteration_number in range(0, 10):
        run(['python', 'vrp.py', 'genetic',
             '-d', f'data/distance_matrix/e{destinations_count}.pickle',
             '-c', 'data/configurations/conf1.json',
             '-v', 'data/vehicles/vehicles1.json',
             '-o', 'data/results/tsp-genetic-0X'])
