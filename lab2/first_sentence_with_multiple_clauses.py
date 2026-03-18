import sys

from core.cleaner import iter_clean_characters
from core.parser import process_sentences
from core.utils import first_sentence_with_multiple_clauses


def main():
    # Szukamy pierwszego zdania, ktore ma wiele czesci
    # i zwracamy tylko jeden wynik.
    process, result = first_sentence_with_multiple_clauses()
    process_sentences(iter_clean_characters(sys.stdin), process)
    print(result())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Błąd: {error}", file=sys.stderr)
        raise SystemExit(1)
