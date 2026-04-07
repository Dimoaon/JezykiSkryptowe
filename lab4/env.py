import os
import sys

def main():
    # sys.argv[0] to nazwa skryptu, więc bierzemy od indeksu 1
    # to są filtry podane przez użytkownika, np. python env.py path home
    filters = sys.argv[1:]

    # os.environ to słownik wszystkich zmiennych środowiskowych
    # .items() zwraca pary (nazwa, wartość)
    env_vars = os.environ.items()

    if filters:
        # list comprehension – tworzymy listę tylko tych zmiennych,
        # których nazwa zawiera przynajmniej jeden z podanych filtrów
        # any() zwraca True jeśli choć jeden warunek jest spełniony
        # .lower() po obu stronach sprawia, że filtr jest case-insensitive
        filtered = [
            (name, value)
            for name, value in env_vars
            if any(f.lower() in name.lower() for f in filters)
        ]
    else:
        # brak filtrów – wyświetlamy wszystkie zmienne
        filtered = list(env_vars)

    # sorted() sortuje alfabetycznie po pierwszym elemencie krotki, czyli po nazwie
    for name, value in sorted(filtered):
        print(f"{name}={value}")

# standardowy idiom Pythona – kod uruchamia się tylko gdy skrypt
# jest wywołany bezpośrednio, a nie importowany jako moduł
if __name__ == "__main__":
    main()
