"""
Zadanie 1 – funkcje parsujące pliki CSV ze stacjami i pomiarami.

Moduł używa biblioteki csv do odczytu danych oraz logging do rejestrowania
informacji o otwieranych plikach i odczytywanych wierszach (wymagane przez zad. 6).
"""

import csv
import logging
from pathlib import Path

log = logging.getLogger(__name__)


def to_float(value: str) -> float | None:
    """Konwertuje napis na float, obsługując polski format z przecinkiem."""
    value = value.strip()
    if not value:
        return None
    return float(value.replace(",", "."))


# ── stacje ────────────────────────────────────────────────────────────────────

def parse_stations(path: Path) -> list[dict]:
    """Parsuje plik stacje.csv i zwraca listę słowników z danymi stacji.

    Klucze słownika odpowiadają nagłówkom kolumn z pliku CSV.
    Znaki nowej linii w nagłówkach są zastępowane spacją (artefakt formatu pliku).
    """
    result = []
    log.info("Otwieranie pliku stacji: %s", path)

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # logujemy rozmiar każdego odczytanego wiersza (zad. 6a)
            log.debug("Odczytano wiersz: %d bajtów", len(",".join(row.values()).encode()))

            # nagłówki mogą zawierać \n (wieloliniowe nazwy kolumn w pliku)
            clean_row = {
                k.replace("\n", " ").strip(): v.strip() if v else ""
                for k, v in row.items()
            }
            result.append(clean_row)

    log.info("Zamknięto plik stacji: %s (%d rekordów)", path, len(result))
    return result


# ── pomiary ───────────────────────────────────────────────────────────────────

def parse_measurement_file(path: Path) -> list[dict]:
    """Parsuje plik pomiarowy i zwraca listę słowników – po jednym na stację.

    Każdy słownik zawiera:
      - metadane stacji: "Kod stacji", "Wskaźnik", "Czas uśredniania" itp.
      - pomiary:         klucz = data (np. "01/01/23 01:00"), wartość = float

    Format pliku (wiersze nagłówkowe przed danymi):
      wiersz 0: Nr, 1, 2, 3, ...
      wiersz 1: Kod stacji, DsCzerStraza, ...
      wiersz 2: Wskaźnik, NO, ...
      wiersz 3: Czas uśredniania, 1g, ...
      wiersz 4: Jednostka, ug/m3, ...
      wiersz 5: Kod stanowiska, ...
      wiersz 6+: DD/MM/YY HH:MM, wartość, wartość, ...
    """
    log.info("Otwieranie pliku pomiarów: %s", path)

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = []

        for r in reader:
            # logujemy rozmiar każdego odczytanego wiersza (zad. 6a)
            log.debug("Odczytano wiersz: %d bajtów", len(",".join(r).encode()))

            # pomijamy całkowicie puste wiersze
            if any(c.strip() for c in r):
                rows.append(r)

    log.info("Zamknięto plik pomiarów: %s", path)

    # szukamy pierwszego wiersza z danymi (zawiera datę w formacie DD/MM/YY)
    data_start = 0
    for i, row in enumerate(rows):
        first = row[0].strip()
        if "/" in first:
            data_start = i
            break

    headers   = rows[:data_start]   # wiersze z metadanymi (Kod stacji, Wskaźnik, ...)
    data_rows = rows[data_start:]   # wiersze z pomiarami  (data, wartość, wartość, ...)

    # liczba kolumn = liczba stacji + 1 (pierwsza kolumna to etykieta wiersza)
    num_cols = max(len(h) for h in headers)

    result = []

    # każda kolumna (od 1) odpowiada jednej stacji
    for col in range(1, num_cols):
        station_dict: dict = {}

        # przepisujemy metadane z nagłówków do słownika stacji
        for h in headers:
            key = h[0].strip()   # np. "Kod stacji", "Wskaźnik"
            if key and col < len(h):
                station_dict[key] = h[col].strip()

        # pomijamy puste kolumny (brak numeru stacji)
        if not station_dict.get("Nr"):
            continue

        # przepisujemy pomiary: data → wartość float
        for row in data_rows:
            if len(row) <= col:
                continue
            date  = row[0].strip()
            value = row[col].strip()
            if not value:
                continue  # brak wartości w tym przedziale – pomijamy
            station_dict[date] = to_float(value)

        result.append(station_dict)

    return result


if __name__ == "__main__":
    base = Path("data")

    stations = parse_stations(base / "stacje.csv")
    print("Stacje:", len(stations))
    print("Pierwsza stacja:", stations[0])

    measurements = parse_measurement_file(base / "measurements" / "2023_PM10_24g.csv")
    print("\nStacje w pomiarach:", len(measurements))
    print("Pierwsza stacja w pomiarach:", {k: v for k, v in list(measurements[0].items())[:8]})
