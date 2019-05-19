import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot


def calculate_temperature(temperature_factor, i):
    return temperature_factor / np.log(i + 2)


def calculate_probability(delta, temperature):
    return np.power(np.e, -1 * delta / temperature)


def get_temperature_trace(iterations, N, color):
    y = [calculate_temperature(N, i) for i in iterations]
    temperature_trace = go.Scatter(
        x=iterations,
        y=y,
        name=f'N = {N}',
        mode='markers',
        marker=dict(size=5, color=color)
    )

    return temperature_trace


def get_probability_trace_const_N(iterations, N, d, color):
    temperatures = [calculate_temperature(N, i) for i in iterations]
    p = [calculate_probability(d, t) for t in temperatures]

    probability_trace = go.Scatter(
        x=iterations,
        y=p,
        name=f'd = {d}',
        mode='markers',
        marker=dict(size=5, color=color)
    )

    return probability_trace


def get_probability_trace_const_d(iterations, N, d, color):
    temperatures = [calculate_temperature(N, i) for i in iterations]
    p = [calculate_probability(d, t) for t in temperatures]

    probability_trace = go.Scatter(
        x=iterations,
        y=p,
        name=f'N = {N}',
        mode='markers',
        marker=dict(size=5, color=color)
    )

    return probability_trace


iterations = list(range(0, 100))
temperature_data = [
    get_temperature_trace(iterations, N=5_000, color='rgb(0,0,0)'),
    get_temperature_trace(iterations, N=10_000, color='rgb(255,0,0)'),
    get_temperature_trace(iterations, N=20_000, color='rgb(0,0,255)')
]
layout = go.Layout(
    legend=dict(orientation="h"),
    xaxis=dict(title='Iteration number: i'),
    yaxis=dict(title='Temperature: T(i, N)')
)
temperature_functions_figure = go.Figure(data=temperature_data, layout=layout)

# Probability
N = 10000
probability_data = [
    get_probability_trace_const_N(iterations, N=N, d=1000, color='rgb(255,0,255)'),
    get_probability_trace_const_N(iterations, N=N, d=2500, color='rgb(0,0,0)'),
    get_probability_trace_const_N(iterations, N=N, d=5000, color='rgb(255,0,0)'),
    get_probability_trace_const_N(iterations, N=N, d=10000, color='rgb(0,255,0)'),
    get_probability_trace_const_N(iterations, N=N, d=20000, color='rgb(0,0,255)')
]
layout = go.Layout(
    legend=dict(orientation="h"),
    xaxis=dict(title='Iteration number: i'),
    yaxis=dict(title=f'Probability: P(i, d, N={N})')
)
probability_figure = go.Figure(data=probability_data, layout=layout)

d = 10000
probability_data_2 = [
    get_probability_trace_const_d(iterations, N=5000, d=d, color='rgb(255,0,255)'),
    get_probability_trace_const_d(iterations, N=10000, d=d, color='rgb(0,0,0)'),
    get_probability_trace_const_d(iterations, N=20000, d=d, color='rgb(255,0,0)'),
    get_probability_trace_const_d(iterations, N=30000, d=d, color='rgb(0,255,0)'),
    get_probability_trace_const_d(iterations, N=50000, d=d, color='rgb(0,0,255)')
]
layout_2 = go.Layout(
    legend=dict(orientation="h"),
    xaxis=dict(title='Iteration number: i'),
    yaxis=dict(title=f'Probability: P(i, d=10000, N)')
)
probability_figure_2 = go.Figure(data=probability_data_2, layout=layout_2)

plot(temperature_functions_figure, filename='temperature_functions.html')
plot(probability_figure, filename='probability_functions_const_N.html')
plot(probability_figure_2, filename='probability_functions_const_d.html')
