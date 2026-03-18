import sys

from core.cleaner import iter_clean_characters
from core.parser import write_first_sentences


def main():
    # Wypisujemy tylko pierwsze 20 zdan,
    # ale nie niszczymy ukladu akapitow.
    write_first_sentences(iter_clean_characters(sys.stdin), sys.stdout, 20)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Błąd: {error}", file=sys.stderr)
        raise SystemExit(1)
