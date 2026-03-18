import sys

from core.cleaner import iter_clean_characters
from core.utils import count_characters


def main():
    # Pobieramy funkcje do liczenia znakow
    # i do odczytu wyniku koncowego.
    process, result = count_characters()

    # Czytamy oczyszczony tekst znak po znaku
    # i przekazujemy go do funkcji liczacej.
    for char in iter_clean_characters(sys.stdin):
        process(char)

    # Na koncu wypisujemy liczbe znakow.
    print(result())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Błąd: {error}", file=sys.stderr)
        raise SystemExit(1)
