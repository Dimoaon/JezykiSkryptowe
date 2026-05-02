# a) forall – czy wszystkie elementy spełniają predykat
def forall(pred, iterable):
    return all(map(pred, iterable))


# b) exists – czy istnieje element spełniający predykat
def exists(pred, iterable):
    return any(map(pred, iterable))


# c) atleast – czy co najmniej n elementów spełnia predykat
def atleast(n, pred, iterable):
    return sum(map(lambda x: 1 if pred(x) else 0, iterable)) >= n


# d) atmost – czy co najwyżej n elementów spełnia predykat
def atmost(n, pred, iterable):
    return sum(map(lambda x: 1 if pred(x) else 0, iterable)) <= n

def main():
    data = [1, 2, 3, 4, 5]

    print("forall:", forall(lambda x: x > 0, data))     # True
    print("exists:", exists(lambda x: x > 4, data))     # True
    print("atleast:", atleast(3, lambda x: x % 2 == 0, data))  # False (2,4 → tylko 2)
    print("atmost:", atmost(2, lambda x: x > 2, data))  # False (3,4,5 → 3 elementy)

if __name__ == "__main__":
    main()