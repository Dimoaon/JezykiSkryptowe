"""
Zadanie 5 & 6 – CLI z argparse i modułem logging.

Uruchomienie:
  python task5.py --quantity NO  --frequency 1g  --start 2023-01-01 --end 2023-01-31 random
  python task5.py --quantity PM10 --frequency 24g --start 2023-06-01 --end 2023-06-30 stats --station DsWrocWybCon
  python task5.py --quantity NO  --frequency 1g  --start 2023-01-01 --end 2023-12-31 anomalies --delta 50
"""

import argparse
import logging
import math
import random
import re
import sys
from datetime import datetime
from pathlib import Path

# funkcje parsujące dane (zad. 1) i grupujące pliki (zad. 2) dostarcza napaarnik
from task1 import parse_stations, parse_measurements
from task2 import group_measurement_files_by_key

# funkcja wykrywania anomalii pochodzi z zadania rozszerzającego 2
from task_ext2 import DEFAULT_BAD_RATIO, DEFAULT_DELTA, detect_anomalies

# ─────────────────────────────────────────────────────────────────────────────
# Zadanie 6 – konfiguracja modułu logging
# ─────────────────────────────────────────────────────────────────────────────

class _MaxLevelFilter(logging.Filter):
    """Filtr przepuszczający tylko logi o poziomie <= max_level.

    Potrzebny dlatego, że StreamHandler domyślnie przepuszcza wszystko
    powyżej ustawionego poziomu – bez tego WARNING trafiałoby i na stdout
    i na stderr jednocześnie.
    """

    def __init__(self, max_level: int):
        super().__init__()
        self._max = max_level

    def filter(self, record: logging.LogRecord) -> bool:
        # zwracamy True tylko gdy poziom nie przekracza progu
        return record.levelno <= self._max


def setup_logging() -> None:
    """Konfiguruje dwa handlery zgodnie z wymaganiami zadania 6:
    - DEBUG / INFO / WARNING → stdout
    - ERROR / CRITICAL       → stderr
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)  # korzeń musi mieć najniższy poziom, handlery filtrują dalej

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(message)s", datefmt="%H:%M:%S"
    )

    # handler dla stdout – przepuszcza do WARNING włącznie
    h_out = logging.StreamHandler(sys.stdout)
    h_out.setLevel(logging.DEBUG)
    h_out.addFilter(_MaxLevelFilter(logging.WARNING))
    h_out.setFormatter(fmt)

    # handler dla stderr – tylko ERROR i CRITICAL
    h_err = logging.StreamHandler(sys.stderr)
    h_err.setLevel(logging.ERROR)
    h_err.setFormatter(fmt)

    root.addHandler(h_out)
    root.addHandler(h_err)


log = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Funkcje pomocnicze
# ─────────────────────────────────────────────────────────────────────────────

def find_measurement_file(mdir: Path, quantity: str, frequency: str) -> Path | None:
    """Wyszukuje plik pomiarowy pasujący do podanej wielkości i częstotliwości.

    Porównanie wielkości jest case-insensitive, bo nazwy plików mogą się
    różnić wielkością liter względem tego, co wpisze użytkownik.
    """
    for (_, q, freq), path in group_measurement_files_by_key(mdir).items():
        if q.upper() == quantity.upper() and freq == frequency:
            return path
    return None


def filter_by_date(
    records: list[tuple[datetime, float | None]],
    start: datetime,
    end: datetime,
) -> list[tuple[datetime, float]]:
    """Filtruje pomiary do podanego przedziału czasowego, pomijając wartości None."""
    return [(dt, v) for dt, v in records if start <= dt <= end and v is not None]


# ─────────────────────────────────────────────────────────────────────────────
# Podkomendy CLI
# ─────────────────────────────────────────────────────────────────────────────

def cmd_random(args, stations, mdata: dict) -> None:
    """Wypisuje nazwę i adres losowej stacji mającej dane w zadanym przedziale."""
    start = datetime.fromisoformat(args.start)
    end   = datetime.fromisoformat(args.end)

    # zbieramy kody stacji, które mają choć jeden pomiar w przedziale
    active_codes = {
        code for code, records in mdata.items()
        if filter_by_date(records, start, end)
    }

    if not active_codes:
        # brak danych dla zadanych parametrów – WARNING bo program może kontynuować
        log.warning(
            "Brak pomiarów dla %s %s w przedziale %s – %s",
            args.quantity, args.frequency, args.start, args.end,
        )
        print("Brak danych dla podanych parametrów.")
        return

    # dopasowujemy kody do metadanych stacji z pliku stacje.csv
    active_stations = [s for s in stations if s.code in active_codes]

    if not active_stations:
        # kody z pliku pomiarowego nie mają odpowiedników w stacje.csv
        log.warning("Aktywne kody stacji nie znaleziono w stacje.csv: %s", active_codes)
        print("Nie znaleziono metadanych dla aktywnych stacji.")
        return

    s = random.choice(active_stations)
    print(f"Nazwa:   {s.name}")
    print(f"Adres:   {s.voivodeship}, {s.city}, {s.address or s.city}")


def cmd_stats(args, stations, mdata: dict) -> None:
    """Oblicza średnią i odchylenie standardowe dla danej stacji i okresu."""
    start = datetime.fromisoformat(args.start)
    end   = datetime.fromisoformat(args.end)

    if args.station not in mdata:
        # stacja nie mierzy tej wielkości – nie jest to błąd krytyczny
        log.warning(
            "Stacja %s nie mierzy %s %s (lub brak danych w pliku)",
            args.station, args.quantity, args.frequency,
        )
        print(f"Stacja '{args.station}' nie ma danych dla {args.quantity} {args.frequency}.")
        return

    records = filter_by_date(mdata[args.station], start, end)

    if not records:
        log.warning(
            "Brak pomiarów dla stacji %s w przedziale %s – %s",
            args.station, args.start, args.end,
        )
        print(f"Brak pomiarów dla stacji '{args.station}' w podanym przedziale.")
        return

    values = [v for _, v in records]
    mean   = sum(values) / len(values)
    # odchylenie standardowe populacyjne (nie próbkowe) – liczymy je ręcznie
    std    = math.sqrt(sum((v - mean) ** 2 for v in values) / len(values))

    info = next((s for s in stations if s.code == args.station), None)
    name = info.name if info else args.station

    print(f"Stacja:       {name} ({args.station})")
    print(f"Wielkość:     {args.quantity}  |  Częstotliwość: {args.frequency}")
    print(f"Przedział:    {args.start} → {args.end}")
    print(f"Pomiary:      {len(values)}")
    print(f"Średnia:      {mean:.4f}")
    print(f"Odch. std.:   {std:.4f}")


def cmd_anomalies(args, stations, mdata: dict) -> None:
    """Wykrywa anomalie w danych pomiarowych dla zadanego okresu."""
    start = datetime.fromisoformat(args.start)
    end   = datetime.fromisoformat(args.end)

    # spłaszczamy słownik stacja→lista w jedną listę krotek (czas, wartość, stacja, wielkość)
    # taki format przyjmuje funkcja detect_anomalies z zadania rozszerzającego 2
    flat = [
        (dt, val, code, args.quantity)
        for code, records in mdata.items()
        if not args.station or code == args.station
        for dt, val in records
        if start <= dt <= end
    ]

    if not flat:
        log.warning("Brak danych do analizy anomalii dla podanych parametrów")
        print("Brak danych do analizy.")
        return

    anomalies = detect_anomalies(
        flat,
        delta_threshold=args.delta,
        bad_ratio_threshold=args.bad_ratio,
    )

    if not anomalies:
        print("Nie wykryto anomalii.")
        return

    station_names = {s.code: s.name for s in stations}
    print(f"Wykryto {len(anomalies)} anomalii:\n")
    for a in anomalies:
        name = station_names.get(a["station"], a["station"])
        print(f"  [{a['type'].upper():10s}] {name}  {a['detail']}")


# ─────────────────────────────────────────────────────────────────────────────
# Walidacja argumentów (zad. 5c)
# ─────────────────────────────────────────────────────────────────────────────

def _valid_date(value: str) -> str:
    """Sprawdza poprawność daty w formacie RRRR-MM-DD."""
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        # rzucamy ArgumentTypeError, żeby argparse wypisał czytelny komunikat
        raise argparse.ArgumentTypeError(
            f"Nieprawidłowa data '{value}' – oczekiwany format: RRRR-MM-DD"
        )


def _valid_quantity(value: str) -> str:
    """Sprawdza, czy wielkość mierzona ma prawidłowy format (litery, cyfry, nawiasy, kropki)."""
    if not re.fullmatch(r"[\w.()\-]+", value):
        raise argparse.ArgumentTypeError(
            f"Nieprawidłowa wielkość '{value}' – użyj np. PM10, PM2.5, NO2, C6H6"
        )
    return value


def _valid_frequency(value: str) -> str:
    """Akceptuje tylko wartości 1g i 24g jako częstotliwość."""
    if value not in ("1g", "24g"):
        raise argparse.ArgumentTypeError(
            f"Nieprawidłowa częstotliwość '{value}' – użyj 1g lub 24g"
        )
    return value


# ─────────────────────────────────────────────────────────────────────────────
# Budowanie parsera CLI (zad. 5)
# ─────────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """Tworzy i zwraca parser argumentów z podkomendami."""
    parser = argparse.ArgumentParser(
        prog="task5.py",
        description="Analizator danych pomiarowych jakości powietrza (dane GIOŚ).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "przykłady:\n"
            "  %(prog)s --quantity NO --frequency 1g "
            "--start 2023-01-01 --end 2023-01-31 random\n"
            "  %(prog)s --quantity PM10 --frequency 24g "
            "--start 2023-06-01 --end 2023-06-30 stats --station DsWrocWybCon\n"
            "  %(prog)s --quantity NO --frequency 1g "
            "--start 2023-01-01 --end 2023-12-31 anomalies --delta 50\n"
        ),
    )

    # argumenty globalne – wymagane dla każdej podkomendy
    parser.add_argument(
        "--data-dir", type=Path, default=Path("data"), metavar="KATALOG",
        help="Katalog z plikami stacje.csv i measurements/ (domyślnie: data/)",
    )
    parser.add_argument(
        "--quantity", required=True, type=_valid_quantity, metavar="WIELKOŚĆ",
        help="Mierzona wielkość, np. PM10, PM2.5, NO, NO2, SO2, C6H6",
    )
    parser.add_argument(
        "--frequency", required=True, type=_valid_frequency, metavar="CZĘST.",
        help="Częstotliwość pomiaru: 1g (godzinowa) lub 24g (dobowa)",
    )
    parser.add_argument(
        "--start", required=True, type=_valid_date, metavar="RRRR-MM-DD",
        help="Początek przedziału czasowego (włącznie)",
    )
    parser.add_argument(
        "--end", required=True, type=_valid_date, metavar="RRRR-MM-DD",
        help="Koniec przedziału czasowego (włącznie)",
    )

    sub = parser.add_subparsers(dest="command", required=True, title="podkomendy")

    # podkomenda: random – losowa stacja z danymi w zadanym przedziale
    sub.add_parser(
        "random",
        help="Wypisuje nazwę i adres losowej stacji mierzącej daną wielkość w przedziale",
    )

    # podkomenda: stats – statystyki dla konkretnej stacji
    sp_stats = sub.add_parser(
        "stats",
        help="Oblicza średnią i odchylenie standardowe dla wskazanej stacji",
    )
    sp_stats.add_argument(
        "--station", required=True, metavar="KOD",
        help="Kod stacji pomiarowej, np. DsWrocWybCon",
    )

    # podkomenda: anomalies – zadanie rozszerzające 2
    sp_an = sub.add_parser(
        "anomalies",
        help="Wykrywa anomalie w danych (złe dane, skoki, przekroczenia progów)",
    )
    sp_an.add_argument(
        "--station", default=None, metavar="KOD",
        help="Ogranicz analizę do jednej stacji (domyślnie: wszystkie)",
    )
    sp_an.add_argument(
        "--delta", type=float, default=DEFAULT_DELTA, metavar="DELTA",
        help=f"Maksymalny dozwolony skok między kolejnymi pomiarami (domyślnie: {DEFAULT_DELTA})",
    )
    sp_an.add_argument(
        "--bad-ratio", type=float, default=DEFAULT_BAD_RATIO, dest="bad_ratio",
        metavar="PRÓG",
        help=f"Maks. udział wartości None/zero/ujemnych (domyślnie: {DEFAULT_BAD_RATIO})",
    )

    return parser


# ─────────────────────────────────────────────────────────────────────────────
# Punkt wejściowy
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    setup_logging()
    args = build_parser().parse_args()

    stations_file = args.data_dir / "stacje.csv"
    meas_dir      = args.data_dir / "measurements"

    # brakujące pliki to błąd krytyczny – program nie może działać bez danych
    if not stations_file.exists():
        log.error("Nie znaleziono pliku stacji: %s", stations_file)
        sys.exit(1)
    if not meas_dir.is_dir():
        log.error("Nie znaleziono katalogu z pomiarami: %s", meas_dir)
        sys.exit(1)

    stations  = parse_stations(stations_file)
    meas_file = find_measurement_file(meas_dir, args.quantity, args.frequency)

    if meas_file is None:
        # brak pliku dla tej wielkości/częstotliwości – WARNING, nie ERROR
        log.warning(
            "Brak pliku pomiarowego dla wielkości='%s' częstotliwość='%s' w %s",
            args.quantity, args.frequency, meas_dir,
        )
        print(f"Brak pliku danych dla '{args.quantity}' z częstotliwością '{args.frequency}'.")
        sys.exit(0)

    mdata = parse_measurements(meas_file)

    # słownik zamiast if/elif – łatwo dodać nowe podkomendy
    dispatch = {
        "random":    cmd_random,
        "stats":     cmd_stats,
        "anomalies": cmd_anomalies,
    }
    dispatch[args.command](args, stations, mdata)


if __name__ == "__main__":
    main()
