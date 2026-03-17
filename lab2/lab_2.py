import sys
from core.cleaner import clean_stream

def main():
    clean_stream(sys.stdin, sys.stdout)

if __name__ == "__main__":
    main()
