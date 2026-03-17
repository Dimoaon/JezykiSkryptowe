import sys
from core.cleaner import clean_text

def main():
    text = sys.stdin.read()
    cleaned = clean_text(text)
    print(cleaned)

if __name__ == "__main__":
    main()