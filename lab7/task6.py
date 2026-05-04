# Zadanie 6 – dekorator @log rejestrujący wywołania funkcji i klas.
# Dekorator przyjmuje poziom logowania jako argument (logging.DEBUG, logging.INFO, itp.).
# Dla funkcji loguje: czas wywołania, nazwę, argumenty, czas trwania, wartość zwróconą.
# Dla klas loguje: moment tworzenia obiektu (wywołanie __init__).

import logging
import time
import functools


# Konfiguracja modułu logging – format z datą i poziomem.
# basicConfig działa tylko jeśli handler nie został jeszcze ustawiony.
import sys

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s [%(levelname)-8s] %(message)s",
    datefmt="%H:%M:%S",
)


def log(level=logging.DEBUG):
    # log() jest fabryką dekoratorów: zwraca właściwy dekorator dla podanego poziomu.
    # Dwupoziomowa struktura (log → decorator → wrapper) jest konieczna, bo dekorator
    # z argumentami musi być wywoływalny na dwa sposoby: @log() i @log(logging.INFO).

    def decorator(obj):
        # Rozróżniamy czy dekorowany obiekt to klasa czy funkcja.
        if isinstance(obj, type):
            return _log_class(obj, level)
        return _log_function(obj, level)

    return decorator


def _log_function(func, level):
    @functools.wraps(func)  # zachowuje __name__, __doc__ itp. oryginalnej funkcji
    def wrapper(*args, **kwargs):
        # Formatujemy argumenty do czytelnego stringa – pozycyjne i słownikowe osobno.
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
    # Dekorujemy __init__ klasy – każde tworzenie obiektu zostanie zalogowane.
    # Nie tworzymy nowej klasy (unikamy problemów z dziedziczeniem i isinstance).
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

@log()                          # poziom domyślny: DEBUG
def add(a, b):
    return a + b


@log(logging.INFO)              # poziom INFO
def multiply(a, b):
    return a * b


@log(logging.WARNING)           # poziom WARNING – widoczny nawet przy wyższym filtrze
def divide(a, b):
    return a / b


@log(logging.INFO)              # dekorowanie klasy – loguje __init__
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @log()                      # metody klasy też można dekorować
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

    rect = Rectangle(5, 3)      # loguje tworzenie obiektu
    rect.area()                 # loguje wywołanie metody
    rect.perimeter()

    print()

    # Funkcja z wieloma typami argumentów
    @log(logging.INFO)
    def greet(name, greeting="Cześć"):
        return f"{greeting}, {name}!"

    greet("Anna")
    greet("Bartek", greeting="Hej")
