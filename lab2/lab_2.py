import sys
from core.cleaner import clean_text
from core.parser import process_sentences
from core.utils import count_sentences

def main():
    text = sys.stdin.read()

    cleaned = clean_text(text)

    process, result = count_sentences()

    process_sentences(cleaned, process)

    print(result())

if __name__ == "__main__":
    main()