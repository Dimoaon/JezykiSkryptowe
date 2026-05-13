# Zadanie 2 – funkcje wyższego rzędu przyjmujące predykat i iterable.

# all/any mają lazy evaluation – zatrzymują się przy pierwszym decydującym elemencie.
def forall(pred, iterable) -> bool:
    return all(map(pred, iterable))


def exists(pred, iterable) -> bool:
    return any(map(pred, iterable))


# sum() zlicza True jak jedynki (True == 1, False == 0).
def atleast(n: int, pred, iterable) -> bool:
    return sum(map(pred, iterable)) >= n


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
