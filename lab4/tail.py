import sys
import os
import time

DEFAULT_LINES = 10

def parse_args():
    args = sys.argv[1:]
    lines = DEFAULT_LINES
    follow = False
    filepath = None

    remaining = []
    for arg in args:
        if arg.startswith("--lines="):
            lines = int(arg.split("=", 1)[1])
        elif arg == "--follow":
            follow = True
        else:
            remaining.append(arg)

    if remaining:
        filepath = remaining[0]

    return lines, follow, filepath

def read_last_lines(lines_list, n):
    return lines_list[-n:] if n < len(lines_list) else lines_list

def tail_file(filepath, n, follow):
    with open(filepath, "r") as f:
        lines = f.readlines()

    for line in read_last_lines(lines, n):
        print(line, end="")

    if follow:
        with open(filepath, "r") as f:
            f.seek(0, 2)  # przejdź na koniec pliku
            while True:
                line = f.readline()
                if line:
                    print(line, end="", flush=True)
                else:
                    time.sleep(0.1)

def tail_stdin(n):
    lines = sys.stdin.readlines()
    for line in read_last_lines(lines, n):
        print(line, end="")

def main():
    n, follow, filepath = parse_args()

    if filepath:
        if not os.path.isfile(filepath):
            print(f"Błąd: plik '{filepath}' nie istnieje.", file=sys.stderr)
            sys.exit(1)
        tail_file(filepath, n, follow)
    elif not sys.stdin.isatty():
        tail_stdin(n)
    else:
        print("Błąd: podaj plik lub dane na wejście standardowe.", file=sys.stderr)
        print("Użycie: python tail.py [--lines=N] [--follow] [plik]", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
