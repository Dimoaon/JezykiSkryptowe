# Zadanie 3 – klasa PasswordGenerator implementująca protokół iteratora.
# Protokół iteratora w Pythonie wymaga dwóch metod: __iter__ i __next__.

import random
import string


class PasswordGenerator:
    def __init__(
        self,
        length: int,
        charset: str = string.ascii_letters + string.digits,  # domyślnie litery + cyfry
        count: int = 10,  # maksymalna liczba haseł do wygenerowania
    ):
        self.length = length
        self.charset = charset
        self.count = count
        self._generated = 0  # licznik – ile haseł już zwrócono

    # __iter__ zwraca sam obiekt – dzięki temu klasa jest jednocześnie iteratorem i iterable.
    # To pozwala używać jej zarówno w pętli for jak i z next().
    def __iter__(self):
        return self

    # __next__ zwraca kolejne hasło lub podnosi StopIteration po wyczerpaniu limitu.
    # random.choices losuje k znaków z charset ze zwracaniem (możliwe powtórzenia).
    def __next__(self) -> str:
        if self._generated >= self.count:
            raise StopIteration  # sygnał dla pętli for że iterator się skończył
        self._generated += 1
        return "".join(random.choices(self.charset, k=self.length))


if __name__ == "__main__":
    gen = PasswordGenerator(length=8, count=3)

    # jawne wywołanie next() – wywołuje __next__ bezpośrednio
    print("Jawne next():")
    print(next(gen))
    print(next(gen))

    # pętla for – kontynuuje od miejsca zatrzymania (1 hasło zostało)
    # for wewnętrznie wywołuje iter() a potem next() w kółko aż do StopIteration
    print("\nfor (1 pozostałe hasło):")
    for pwd in gen:
        print(pwd)

    # nowy generator z niestandardowym zestawem znaków
    print("\nNowy generator (tylko wielkie litery, 5 haseł po 12 znaków):")
    for pwd in PasswordGenerator(length=12, charset=string.ascii_uppercase, count=5):
        print(pwd)

    # test StopIteration po wyczerpaniu
    print("\nTest StopIteration:")
    exhausted = PasswordGenerator(length=4, count=1)
    print(next(exhausted))
    try:
        next(exhausted)
    except StopIteration:
        print("StopIteration – generator wyczerpany.")
