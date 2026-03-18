import sys

from core.cleaner import iter_clean_characters
from core.parser import process_sentences
from core.utils import longest_sentence_no_same_start_letters


def main():
    # Tu szukamy najdluzszego zdania spelniajacego dodatkowy warunek:
    # zadne dwa sasiednie slowa nie moga zaczynac sie ta sama litera.
    process, result = longest_sentence_no_same_start_letters()
    process_sentences(iter_clean_characters(sys.stdin), process)
    print(result())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Błąd: {error}", file=sys.stderr)
        raise SystemExit(1)
