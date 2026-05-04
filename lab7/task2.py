# Zadanie 2 – funkcje wyższego rzędu przyjmujące predykat i iterable.
# pred – funkcja jednoargumentowa zwracająca True/False (predykat).
# Wszystkie implementacje opierają się na wbudowanych funkcjach funkcyjnych Pythona.


# forall – odpowiednik logicznego "dla każdego" (∀).
# all() zwraca True tylko jeśli wszystkie elementy są prawdziwe.
# map(pred, iterable) aplikuje predykat do każdego elementu – dostajemy listę bool.
def forall(pred, iterable) -> bool:
    return all(map(pred, iterable))


# exists – odpowiednik logicznego "istnieje" (∃).
# any() zwraca True jeśli choć jeden element jest prawdziwy – i od razu się zatrzymuje.
def exists(pred, iterable) -> bool:
    return any(map(pred, iterable))


# atleast – co najmniej n elementów spełnia predykat.
# sum() na liście bool zlicza True (True == 1, False == 0).
def atleast(n: int, pred, iterable) -> bool:
    return sum(map(pred, iterable)) >= n


# atmost – co najwyżej n elementów spełnia predykat.
# Ta sama technika: zliczamy True i sprawdzamy czy nie przekraczamy n.
def atmost(n: int, pred, iterable) -> bool:
    return sum(map(pred, iterable)) <= n


if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    is_even = lambda x: x % 2 == 0
    is_positive = lambda x: x > 0
    is_big = lambda x: x > 10

    print("forall(is_positive, [1,2,3,4,5]):", forall(is_positive, data))  # True
    print("forall(is_even,     [1,2,3,4,5]):", forall(is_even, data))      # False

    print("exists(is_even,     [1,2,3,4,5]):", exists(is_even, data))      # True
    print("exists(is_big,      [1,2,3,4,5]):", exists(is_big, data))       # False

    print("atleast(2, is_even, [1,2,3,4,5]):", atleast(2, is_even, data))  # True  (2 i 4)
    print("atleast(3, is_even, [1,2,3,4,5]):", atleast(3, is_even, data))  # False

    print("atmost(2, is_even,  [1,2,3,4,5]):", atmost(2, is_even, data))   # True
    print("atmost(1, is_even,  [1,2,3,4,5]):", atmost(1, is_even, data))   # False
