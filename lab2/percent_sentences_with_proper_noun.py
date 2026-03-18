import sys

from core.cleaner import iter_clean_characters
from core.parser import process_sentences
from core.utils import percent_sentences_with_proper_noun


def main():
    # Liczymy procent zdan, w ktorych pojawia sie nazwa wlasna.
    process, result = percent_sentences_with_proper_noun()
    process_sentences(iter_clean_characters(sys.stdin), process)
    print(result())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Błąd: {error}", file=sys.stderr)
        raise SystemExit(1)
