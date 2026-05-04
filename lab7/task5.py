# Zadanie 5 – make_generator_mem() z memoizacją przez functools.
# Działa jak make_generator() z task4, ale przed wyliczeniem f(n) sprawdza cache.
# Memoizacja szczególnie pomaga przy funkcjach rekurencyjnych (np. Fibonacci),
# gdzie te same wartości są obliczane wielokrotnie bez cache'u.
#
# Strategia bez duplikowania kodu: dekorujemy f przez lru_cache, a potem przekazujemy
# udekorowaną wersję do make_generator() z task4 – bo logika generatora jest identyczna.

from functools import lru_cache
from task4 import make_generator


def make_generator_mem(f):
    # lru_cache(maxsize=None) to nieograniczony cache – zapamiętuje wynik dla każdego n.
    # wraps=None nie jest potrzebne; dekorujemy zwykłą funkcję wewnętrzną.
    # UWAGA: lru_cache wymaga, żeby argumenty były hashowalne (int – tak jest).
    f_mem = lru_cache(maxsize=None)(f)
    return make_generator(f_mem)


# ---------- wersja z rekurencją + memoizacja „z zewnątrz" ----------
# Gdy f sama jest rekurencyjna (np. fibonacci), memoizacja przez lru_cache na
# zewnętrznym wywołaniu NIE przyspiesza wewnętrznych wywołań rekurencyjnych
# (bo te wołają oryginalną, nieopakowaną funkcję).
# Rozwiązanie: opakować f_mem w środku tak, by rekurencja używała już cache'owanej wersji.

def fibonacci_mem(n: int) -> int:
    # Wersja z własnym, wewnętrznym cache'em – rekurencja wewnątrz też korzysta z cache.
    @lru_cache(maxsize=None)
    def fib(k):
        return 1 if k <= 2 else fib(k - 1) + fib(k - 2)
    return fib(n)


def catalan_mem(n: int) -> int:
    # C(n) = sum_{i=0}^{n-1} C(i)*C(n-1-i), C(0) = 1 – definicja rekurencyjna.
    # lru_cache wewnątrz sprawia, że każde C(k) liczymy tylko raz.
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
