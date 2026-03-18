import sys
from core.cleaner import clean_stream
from core.parser import process_sentences
from core.utils import (
    count_words,
    count_characters,
    percent_sentences_with_proper_noun,
    longest_sentence,
    filter_sentences_max_4_words,
    first_20_sentences,
    count_paragraphs
)

def main():
    # czyszczenie tekstu
    from io import StringIO
    cleaned = StringIO()
    clean_stream(sys.stdin, cleaned)
    cleaned.seek(0)

    print("Redukujace: ")

    # count_words
    process, result = count_words()
    process_sentences(cleaned, process)
    print("Liczba słów:", result())

    cleaned.seek(0)

    # count_characters
    process, result = count_characters()
    process_sentences(cleaned, process)
    print("Znaki (bez spacji):", result())

    cleaned.seek(0)

    # percent_sentences_with_proper_noun
    process, result = percent_sentences_with_proper_noun()
    process_sentences(cleaned, process)
    print("Zdania z nazwami własnymi (%):", result())

    print("\nWyszukujace: ")

    cleaned.seek(0)

    # longest_sentence
    process, result = longest_sentence()
    process_sentences(cleaned, process)
    print("Najdłuższe zdanie:")
    print(result())

    print("\nFiltrujace: ")

    cleaned.seek(0)

    # filter max 4 words
    process = filter_sentences_max_4_words()

    def printer(sentence):
        res = process(sentence)
        if res:
            print(res)

    process_sentences(cleaned, printer)

    print("\nPipeline")

    cleaned.seek(0)

    # filtr
    filter_process = first_20_sentences()

    # redukcja
    char_process, char_result = count_paragraphs()

    def pipeline(sentence):
        res = filter_process(sentence)
        if res:
            for c in res:
                char_process(c)
            char_process("\n")

    process_sentences(cleaned, pipeline)

    print("Akapity w pierwszych 20 zdaniach:", char_result())


if __name__ == "__main__":
    main()