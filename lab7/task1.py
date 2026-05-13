# Zadanie 1 – implementacje funkcji bez użycia pętli for/while ani instrukcji if
# (dozwolone są list/dict comprehensions oraz operator trójargumentowy).

from functools import reduce


# a) Bierzemy pierwszą literę każdego słowa i sklejamy w jeden string.
def acronym(words: list[str]) -> str:
    return "".join(map(lambda w: w[0].upper(), words))


# b) Sortujemy listę; operator trójargumentowy wybiera środkowy element (lub średnią dwóch).
def median(lst: list[float]) -> float:
    s = sorted(lst)
    n = len(s)
    return s[n // 2] if n % 2 != 0 else (s[n // 2 - 1] + s[n // 2]) / 2


# c) Rekurencja zastępuje pętlę while; wzór Newtona: y_new = (y + x/y) / 2.
def pierwiastek(x: float, epsilon: float, y: float | None = None) -> float:
    y = x / 2 if y is None else y
    return y if abs(y * y - x) < epsilon else pierwiastek(x, epsilon, (y + x / y) / 2)


# d) dict.fromkeys() zbiera unikalne litery zachowując kolejność pierwszego wystąpienia.
def make_alpha_dict(text: str) -> dict[str, list[str]]:
    words = text.split()
    chars = dict.fromkeys(c for w in words for c in w if c.isalpha())
    return {c: [w for w in words if c in w] for c in chars}


# e) reduce() spłaszcza rekurencyjnie – działa na dowolnym poziomie zagnieżdżenia.
def flatten(lst: list) -> list:
    return reduce(
        lambda acc, x: acc + (flatten(x) if isinstance(x, (list, tuple)) else [x]),
        lst,
        [],
    )


# f) Klucz kanoniczny: litery posortowane → anagramy mają ten sam klucz.
def group_anagrams(words: list[str]) -> dict[str, list[str]]:
    key = lambda w: "".join(sorted(w))
    return reduce(
        lambda d, w: {**d, key(w): d.get(key(w), []) + [w]},
        words,
        {},
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
