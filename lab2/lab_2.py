import sys
from core.parser import process_sentences
from core.cleaner import clean_text

def print_sentence(sentence):
    print(">>", sentence)

def main():
    text = sys.stdin.read()
    cleaned = clean_text(text)

    process_sentences(cleaned, print_sentence)

if __name__ == "__main__":
    main()