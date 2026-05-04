# Zadanie 4 – make_generator() za pomocą domknięcia (closure).
# Funkcja make_generator() przyjmuje jednoargumentową funkcję f
# i zwraca generator obliczający f(1), f(2), f(3), … bez końca.
# Zamiast klasy z __next__ używamy składni `yield` – Python sam tworzy obiekt generatora.

from math import factorial


def make_generator(f):
    # Wewnętrzna funkcja generatorowa: `yield` zawiesza wykonanie i zwraca wartość
    # do wywołującego; przy kolejnym next() wznawia od miejsca zawieszenia.
    # Domknięcie (closure) – wewnętrzna funkcja „pamięta" f z zewnętrznego zakresu.
    def generator():
        n = 1
        while True:          # generator nieskończony – StopIteration przez next() na zewnątrz
            yield f(n)
            n += 1
    return generator()       # zwracamy gotowy obiekt generatora, nie samą funkcję


# ---------- pomocnicze funkcje do testów ----------

def fibonacci(n: int) -> int:
    # n-ta liczba Fibonacciego (F(1)=1, F(2)=1, F(3)=2, …) – wariant rekurencyjny.
    # Wolny dla dużych n, ale wystarczający do demonstracji (memoizacja w task5.py).
    return 1 if n <= 2 else fibonacci(n - 1) + fibonacci(n - 2)


def catalan(n: int) -> int:
    # n-ta liczba Catalana: C(n) = (2n)! / ((n+1)! * n!)
    # C(1)=1, C(2)=2, C(3)=5, C(4)=14, …
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
