from functools import wraps
from time import time


def timer(decorated_function):
    @wraps(decorated_function)
    def wrapper(*args, **kwargs):
        start = time()
        result = decorated_function(*args, **kwargs)
        end = time()
        print(f'Algorithm needed {end-start} seconds to solve the problem.')

        return result

    return wrapper
