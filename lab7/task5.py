# Zadanie 5 – make_generator_mem() z memoizacją przez functools.lru_cache.
# Bez duplikowania kodu: opakowujemy f przez lru_cache i przekazujemy do make_generator.

from functools import lru_cache
from task4 import make_generator


def make_generator_mem(f):
    return make_generator(lru_cache(maxsize=None)(f))


# lru_cache na zewnątrz NIE wystarczy dla funkcji rekurencyjnych – rekurencja woła oryginał.
# Rozwiązanie: cache wewnątrz funkcji, żeby wywołania rekurencyjne też z niego korzystały.

def fibonacci_mem(n: int) -> int:
    @lru_cache(maxsize=None)
    def fib(k):
        return 1 if k <= 2 else fib(k - 1) + fib(k - 2)
    return fib(n)


def catalan_mem(n: int) -> int:
    @lru_cache(maxsize=None)
    def cat(k):
        return 1 if k == 0 else sum(cat(i) * cat(k - 1 - i) for i in range(k))
    return cat(n)


if __name__ == "__main__":
    import itertools, time

    # --- porównanie szybkości: Fibonacci bez/z memoizacją ---
    def fibonacci_slow(n):
        return 1 if n <= 2 else fibonacci_slow(n - 1) + fibonacci_slow(n - 2)

    n_test = 30
    t0 = time.perf_counter()
    list(itertools.islice(make_generator(fibonacci_slow), n_test))
    t_slow = time.perf_counter() - t0

    t0 = time.perf_counter()
    list(itertools.islice(make_generator_mem(fibonacci_mem), n_test))
    t_fast = time.perf_counter() - t0

    print(f"Fibonacci({n_test}) bez memoizacji: {t_slow:.4f}s")
    print(f"Fibonacci({n_test}) z  memoizacją: {t_fast:.4f}s")
    print(f"Przyspieszenie: ~{t_slow / max(t_fast, 1e-9):.0f}x\n")

    # --- wartości Fibonacciego z memoizacją ---
    fibs = make_generator_mem(fibonacci_mem)
    print("Fibonacci mem (pierwsze 10):", list(itertools.islice(fibs, 10)))

    # --- wartości Catalana z memoizacją ---
    cats = make_generator_mem(catalan_mem)
    print("Catalana  mem (pierwsze  8):", list(itertools.islice(cats, 8)))

    # --- lambdy też działają (są hashowalne jako obiekty) ---
    cubes = make_generator_mem(lambda n: n ** 3)
    print("Sześciany     (pierwsze  6):", list(itertools.islice(cubes, 6)))
