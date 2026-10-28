"""Retry com backoff exponencial."""
import functools
import time


def retry(attempts: int = 3, base_delay: float = 0.5, exceptions: tuple = (Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if i == attempts - 1:
                        raise
                    time.sleep(base_delay * (2 ** i))
        return wrapper
    return decorator
