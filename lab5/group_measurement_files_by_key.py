"""
Zadanie 2 – grupowanie plików pomiarowych za pomocą wyrażeń regularnych.

Funkcja przeszukuje podany katalog i dla każdego pliku pasującego do wzorca
<rok>_<wielkość>_<częstotliwość>.csv zwraca wpis w słowniku.
"""

import re
from pathlib import Path


def group_measurement_files_by_key(path: Path) -> dict[tuple[str, str, str], Path]:
    """Zwraca słownik {(rok, wielkość, częstotliwość): Path} dla plików w katalogu.

    Funkcja przeszukuje tylko pliki bezpośrednio w podanym katalogu (nie rekurencyjnie).
    Pliki niespełniające wzorca są ignorowane.

    Wzorzec nazwy pliku: <rok>_<wielkość>_<częstotliwość>.csv
      - rok          – 4 cyfry, np. 2023
      - wielkość     – dowolny ciąg znaków, np. PM10, NO, As(PM10), Jony_PM25
      - częstotliwość – 1g, 24g lub 1m
    """
    # regex zamiast split() – wymagane przez treść zadania 2
    # ^(\d{4})   – kotwica początku + rok (dokładnie 4 cyfry)
    # _(.+)_     – zachłanne .+ dopasowuje całą nazwę wielkości łącznie z podkreślnikami
    #              np. "Jony_PM25" w pliku 2023_Jony_PM25_24g.csv
    #              zachłanność jest tu pożądana – bierzemy wszystko między pierwszym
    #              a ostatnim podkreślnikiem
    # (1g|24g|1m) – dozwolone częstotliwości jako alternatywa
    # \.csv$     – dosłowna kropka (bez \ byłaby dzikim znakiem) + kotwica końca
    pattern = re.compile(r"^(\d{4})_(.+)_(1g|24g|1m)\.csv$")

    result: dict[tuple[str, str, str], Path] = {}

    for file_path in path.iterdir():
        if not file_path.is_file():
            continue  # pomijamy podkatalogi

        m = pattern.match(file_path.name)
        if m:
            key = (m.group(1), m.group(2), m.group(3))  # (rok, wielkość, częstotliwość)
            result[key] = file_path

    return result


if __name__ == "__main__":
    import sys
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/measurements")

    grouped = group_measurement_files_by_key(base)

    print("Znalezione pliki:\n")
    for key, path in sorted(grouped.items()):
        print(f"  {key} -> {path.name}")

    print(f"\nŁącznie: {len(grouped)} plików")
