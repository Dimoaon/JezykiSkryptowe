# Zadanie 4 – make_generator() za pomocą domknięcia (closure).
# Wewnętrzna funkcja z yield tworzy obiekt generatora i „pamięta" f z zewnętrznego zakresu.

from math import factorial


def make_generator(f):
    def generator():
        n = 1
        while True:
            yield f(n)  # yield zawiesza wykonanie i zwraca wartość; next() wznawia
            n += 1
    return generator()


def fibonacci(n: int) -> int:
    # rekurencja bez memoizacji – wolna dla dużych n (patrz task5)
    return 1 if n <= 2 else fibonacci(n - 1) + fibonacci(n - 2)


def catalan(n: int) -> int:
    # C(n) = (2n)! / ((n+1)! * n!)
    return factorial(2 * n) // (factorial(n + 1) * factorial(n))


if __name__ == "__main__":
    import itertools

    # Liczby kwadratów: 1, 4, 9, 16, 25, …
    squares = make_generator(lambda n: n ** 2)
    print("Kwadraty (pierwsze 7):", list(itertools.islice(squares, 7)))

    # Liczby Fibonacciego: 1, 1, 2, 3, 5, 8, 13, …
    fibs = make_generator(fibonacci)
    print("Fibonacci (pierwsze 8):", list(itertools.islice(fibs, 8)))

    # Liczby Catalana: 1, 2, 5, 14, 42, …
    catalans = make_generator(catalan)
    print("Catalana  (pierwsze 6):", list(itertools.islice(catalans, 6)))

    # Liczby trójkątne: n*(n+1)/2 → 1, 3, 6, 10, 15, …
    triangular = make_generator(lambda n: n * (n + 1) // 2)
    print("Trójkątne (pierwsze 6):", list(itertools.islice(triangular, 6)))

    # next() – jawne pobieranie wartości z generatora
    print("\nJawne next() na nowym generatorze kwadratów:")
    g = make_generator(lambda n: n ** 2)
    print(next(g), next(g), next(g))  # 1 4 9
