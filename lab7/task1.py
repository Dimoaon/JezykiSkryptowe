# Zadanie 1 – implementacje funkcji bez użycia pętli for/while ani instrukcji if
# (dozwolone są list/dict comprehensions oraz operator trójargumentowy).

from functools import reduce


# a) Akronim – bierzemy pierwszą literę każdego słowa i zamieniamy na wielką.
# map() aplikuje lambdę do każdego elementu listy, join() skleja wyniki w jeden string.
def acronym(words: list[str]) -> str:
    return "".join(map(lambda w: w[0].upper(), words))


# b) Mediana – sortujemy listę, a potem patrzymy na środkowy element.
# Jeśli liczba elementów nieparzysta – środkowy element to mediana.
# Jeśli parzysta – uśredniamy dwa środkowe elementy.
# Operator trójargumentowy (a if cond else b) zastępuje instrukcję if.
def median(lst: list[float]) -> float:
    s = sorted(lst)
    n = len(s)
    return s[n // 2] if n % 2 != 0 else (s[n // 2 - 1] + s[n // 2]) / 2


# c) Pierwiastek metodą Newtona – zamiast pętli while używamy rekurencji.
# Wzór: nowe przybliżenie = (y + x/y) / 2
# Startujemy od y = x/2 (domyślny argument), powtarzamy aż błąd < epsilon.
# Warunek stopu: |y² - x| < epsilon, też przez operator trójargumentowy.
def pierwiastek(x: float, epsilon: float, y: float | None = None) -> float:
    y = x / 2 if y is None else y
    return y if abs(y * y - x) < epsilon else pierwiastek(x, epsilon, (y + x / y) / 2)


# d) Słownik litera → słowa zawierające tę literę.
# dict.fromkeys() zbiera unikalne litery zachowując kolejność pierwszego wystąpienia.
# Następnie dict comprehension dla każdej litery filtruje słowa ją zawierające.
def make_alpha_dict(text: str) -> dict[str, list[str]]:
    words = text.split()
    # generator expression wewnątrz dict.fromkeys – odpowiednik podwójnej pętli for
    chars = dict.fromkeys(c for w in words for c in w if c.isalpha())
    return {c: [w for w in words if c in w] for c in chars}


# e) Spłaszczanie listy – działa na dowolnym poziomie zagnieżdżenia.
# reduce() przetwarza listę element po elemencie, akumulując wynik w acc.
# Jeśli element jest listą lub krotką – rekurencyjnie spłaszczamy go dalej.
# Jeśli element skalarny – po prostu dodajemy go do akumulatora.
def flatten(lst: list) -> list:
    return reduce(
        lambda acc, x: acc + (flatten(x) if isinstance(x, (list, tuple)) else [x]),
        lst,
        [],  # akumulator startowy – pusta lista
    )


# f) Grupowanie anagramów – kluczem jest słowo z literami posortowanymi alfabetycznie.
# "kot" i "tok" mają ten sam klucz "kot", więc trafiają do jednej grupy.
# reduce() buduje słownik krok po kroku: dla każdego słowa oblicza klucz,
# a potem dopisuje słowo do istniejącej listy (lub tworzy nową przez d.get(..., [])).
def group_anagrams(words: list[str]) -> dict[str, list[str]]:
    key = lambda w: "".join(sorted(w))  # klucz kanoniczny: litery posortowane
    return reduce(
        lambda d, w: {**d, key(w): d.get(key(w), []) + [w]},
        words,
        {},  # akumulator startowy – pusty słownik
    )


if __name__ == "__main__":
    print("a) acronym:")
    print(acronym(["Zakład", "Ubezpieczeń", "Społecznych"]))  # ZUS

    print("\nb) median:")
    print(median([1, 1, 19, 2, 3, 4, 4, 5, 1]))  # 3

    print("\nc) pierwiastek Newtona:")
    print(pierwiastek(3, epsilon=0.1))   # 1.75
    print(pierwiastek(9, epsilon=0.01))  # ~3.00009...

    print("\nd) make_alpha_dict:")
    print(make_alpha_dict("on i ona"))
    # {'o': ['on', 'ona'], 'n': ['on', 'ona'], 'i': ['i'], 'a': ['ona']}

    print("\ne) flatten:")
    print(flatten([1, [2, 3], [[4, 5], 6]]))  # [1, 2, 3, 4, 5, 6]

    print("\nf) group_anagrams:")
    print(group_anagrams(["kot", "tok", "pies", "kep", "pek"]))
    # {'kot': ['kot', 'tok'], 'eips': ['pies'], 'ekp': ['kep', 'pek']}
