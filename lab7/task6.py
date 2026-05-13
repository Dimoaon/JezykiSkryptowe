# Zadanie 6 – dekorator @log logujący wywołania funkcji i tworzenie obiektów klas.
# Trójpoziomowa struktura (log → decorator → wrapper) potrzebna, bo dekorator przyjmuje argument.
# isinstance(obj, type) rozróżnia klasę od funkcji.

import logging
import time
import functools
import sys

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s [%(levelname)-8s] %(message)s",
    datefmt="%H:%M:%S",
)


def log(level=logging.DEBUG):
    def decorator(obj):
        if isinstance(obj, type):
            return _log_class(obj, level)
        return _log_function(obj, level)
    return decorator


def _log_function(func, level):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        call_time = time.strftime("%H:%M:%S")
        t_start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - t_start

        logging.log(
            level,
            f"[{call_time}] {func.__name__}({signature}) "
            f"→ {result!r}  ({duration * 1000:.2f} ms)",
        )
        return result
    return wrapper


def _log_class(cls, level):
    # Modyfikujemy __init__ zamiast tworzyć nową klasę – unikamy problemów z isinstance.
    original_init = cls.__init__

    @functools.wraps(original_init)
    def new_init(self, *args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        t_start = time.perf_counter()
        original_init(self, *args, **kwargs)
        duration = time.perf_counter() - t_start

        logging.log(
            level,
            f"Utworzono obiekt {cls.__name__}({signature})  ({duration * 1000:.2f} ms)",
        )

    cls.__init__ = new_init
    return cls


# ---------- demonstracja ----------

@log()
def add(a, b):
    return a + b


@log(logging.INFO)
def multiply(a, b):
    return a * b


@log(logging.WARNING)
def divide(a, b):
    return a / b


@log(logging.INFO)
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @log()
    def area(self):
        return self.width * self.height

    @log(logging.DEBUG)
    def perimeter(self):
        return 2 * (self.width + self.height)


if __name__ == "__main__":
    print("=== Dekorator @log – demonstracja ===\n")

    add(3, 4)
    multiply(6, 7)
    divide(10, 4)

    print()

    rect = Rectangle(5, 3)
    rect.area()
    rect.perimeter()

    print()

    @log(logging.INFO)
    def greet(name, greeting="Cześć"):
        return f"{greeting}, {name}!"

    greet("Anna")
    greet("Bartek", greeting="Hej")
