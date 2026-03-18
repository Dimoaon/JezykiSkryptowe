import sys

from core.cleaner import iter_clean_characters
from core.utils import count_paragraphs


def main():
    # Tworzymy licznik akapitow.
    process, result = count_paragraphs()

    # Cleaner daje nam juz tekst bez preambuly i bez stopki wydawniczej.
    for char in iter_clean_characters(sys.stdin):
        process(char)

    # Wypisujemy liczbe akapitow.
    print(result())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Błąd: {error}", file=sys.stderr)
        raise SystemExit(1)
