from functools import wraps
from time import time


def timer(decorated_function):
    @wraps(decorated_function)
    def wrapper(*args, **kwargs):
        start = time()
        result = decorated_function(*args, **kwargs)
        end = time()
        print(f'Algorithm took {end - start} seconds to perform.')

        return result

    return wrapper
