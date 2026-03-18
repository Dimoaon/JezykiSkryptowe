import sys
from core.cleaner import clean_stream


def main():
    # Glowny skrypt z punktu 2 PDF:
    # czyta tekst ze stdin, czyści go i wypisuje wynik na stdout.
    clean_stream(sys.stdin, sys.stdout)
    return 0


if __name__ == "__main__":
    try:
        # Uruchamiamy funkcje main tylko wtedy,
        # gdy plik jest odpalany jako skrypt z terminala.
        raise SystemExit(main())
    except Exception as error:
        # W razie bledu pokazujemy czytelny komunikat zamiast tracebacka.
        print(f"Błąd: {error}", file=sys.stderr)
        raise SystemExit(1)
