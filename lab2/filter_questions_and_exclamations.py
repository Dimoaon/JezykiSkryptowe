import sys

from core.cleaner import iter_clean_characters
from core.parser import process_sentences
from core.utils import filter_questions_and_exclamations


def main():
    # Ta funkcja przepuszcza tylko pytania i wykrzyknienia.
    process = filter_questions_and_exclamations()

    def handle_sentence(sentence):
        # Parser daje nam jedno zdanie,
        # a filtr decyduje, czy je wypisac.
        result = process(sentence)
        if result:
            print(result)

    process_sentences(iter_clean_characters(sys.stdin), handle_sentence)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Błąd: {error}", file=sys.stderr)
        raise SystemExit(1)
