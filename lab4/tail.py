import sys
import os
import time

DEFAULT_LINES = 10

def parse_args():
    # pomijamy sys.argv[0] (nazwa skryptu), bierzemy resztę
    args = sys.argv[1:]
    lines = DEFAULT_LINES
    follow = False
    filepath = None

    remaining = []
    for arg in args:
        if arg.startswith("--lines="):
            # split z maxsplit=1 bezpiecznie oddziela nazwę parametru od wartości
            lines = int(arg.split("=", 1)[1])
        elif arg == "--follow":
            follow = True
        else:
            # wszystko co nie jest flagą, traktujemy jako ścieżkę do pliku
            remaining.append(arg)

    if remaining:
        filepath = remaining[0]

    return lines, follow, filepath

def read_last_lines(lines_list, n):
    # wycinanie ostatnich n elementów listy
    # jeśli n >= długość listy, zwracamy całą listę
    return lines_list[-n:] if n < len(lines_list) else lines_list

def tail_file(filepath, n, follow):
    with open(filepath, "r") as f:
        lines = f.readlines()

    # wypisujemy ostatnie n linii
    for line in read_last_lines(lines, n):
        print(line, end="")  # end="" bo linie już mają "\n" na końcu

    if follow:
        # otwieramy plik ponownie i ustawiamy kursor na jego końcu
        with open(filepath, "r") as f:
            f.seek(0, 2)  # 0 bajtów od końca pliku (os.SEEK_END = 2)
            while True:
                line = f.readline()
                if line:
                    # nowa linia pojawiła się w pliku – wypisujemy ją
                    print(line, end="", flush=True)
                else:
                    # brak nowych danych – czekamy chwilę zanim sprawdzimy ponownie
                    time.sleep(0.1)

def tail_stdin(n):
    # czytamy wszystkie linie ze standardowego wejścia naraz
    lines = sys.stdin.readlines()
    for line in read_last_lines(lines, n):
        print(line, end="")

def main():
    n, follow, filepath = parse_args()

    if filepath:
        # jeśli podano ścieżkę do pliku – ignorujemy stdin (zgodnie z treścią zadania)
        if not os.path.isfile(filepath):
            print(f"Błąd: plik '{filepath}' nie istnieje.", file=sys.stderr)
            sys.exit(1)
        tail_file(filepath, n, follow)
    elif not sys.stdin.isatty():
        # sys.stdin.isatty() zwraca False gdy dane są przesyłane przez pipe
        # czyli gdy ktoś zrobił: cat plik.txt | python tail.py
        tail_stdin(n)
    else:
        print("Błąd: podaj plik lub dane na wejście standardowe.", file=sys.stderr)
        print("Użycie: python tail.py [--lines=N] [--follow] [plik]", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
