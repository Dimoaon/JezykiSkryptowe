from functools import reduce

# a) Akronim
def acronym(words):
    return ''.join(map(lambda w: w[0].upper(), words))


# b) Mediana
def median(nums):
    s = sorted(nums)
    n = len(s)
    mid = n // 2
    return (s[mid] if n % 2 == 1 else (s[mid - 1] + s[mid]) / 2)


# c) Pierwiastek Newtona (rekurencyjnie, bez while)
def pierwiastek(x, epsilon=1e-6):

    def newton(y):
        return (y + x / y) / 2

    def iterate(y):
        return y if abs(y*y - x) < epsilon else iterate(newton(y))

    return iterate(x / 2 if x != 0 else 0)


# d) Słownik znak -> lista słów zawierających znak
def make_alpha_dict(text):
    words = text.split()
    chars = set(filter(lambda c: c.isalpha(), text))
    return {
        c: list(filter(lambda w: c in w, words))
        for c in chars
    }


# e) Spłaszczanie list (rekurencja)
def flatten(lst):
    return list(
        reduce(
            lambda acc, x: acc + (flatten(x) if isinstance(x, (list, tuple)) else [x]),
            lst,
            [])
    )


# f) Grupowanie anagramów
def group_anagrams(words):
    key = lambda w: ''.join(sorted(w))
    return reduce(
        lambda acc, w: {
            **acc,
            key(w): acc.get(key(w), []) + [w]
        },
        words,
        {}
    )

def main():
    print("=== a) acronym ===")
    print(acronym(["Zakład", "Ubezpieczeń", "Społecznych"]))  # ZUS

    print("\n=== b) median ===")
    print(median([1, 1, 19, 2, 3, 4, 4, 5, 1]))  # 3
    print(median([1, 2, 3, 4]))  # 2.5 (parzysta liczba elementów)

    print("\n=== c) pierwiastek (Newton) ===")
    print(pierwiastek(3, epsilon=0.1))   # ~1.75
    print(pierwiastek(9, epsilon=0.0001))  # ~3

    print("\n=== d) make_alpha_dict ===")
    print(make_alpha_dict("on i ona"))
    # {'o': ['on', 'ona'], 'n': ['on', 'ona'], 'i': ['i'], 'a': ['ona']}

    print("\n=== e) flatten ===")
    print(flatten([1, [2, 3], [[4, 5], 6]]))  # [1,2,3,4,5,6]
    print(flatten([1, (2, 3), [4, (5, 6)]]))  # działa też dla tuple

    print("\n=== f) group_anagrams ===")
    print(group_anagrams(["kot", "tok", "pies", "kep", "pek"]))
    # {'kot': ['kot', 'tok'], 'eips': ['pies'], 'ekp': ['kep', 'pek']}


if __name__ == "__main__":
    main()