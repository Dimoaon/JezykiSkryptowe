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

# parsowanie plików CSV dostarcza moduł z zadania 1
from parser import parse_stations, parse_measurement_file

# grupowanie plików pomiarowych regex'em – zadanie 2
from group_measurement_files_by_key import group_measurement_files_by_key

# funkcja wykrywania anomalii – zadanie rozszerzające 2
from task_ext2 import DEFAULT_BAD_RATIO, DEFAULT_DELTA, detect_anomalies


# ─────────────────────────────────────────────────────────────────────────────
# Zadanie 6 – konfiguracja modułu logging
# ─────────────────────────────────────────────────────────────────────────────

class _MaxLevelFilter(logging.Filter):
    """Filtr zatrzymujący logi powyżej podanego poziomu.

    Problem: StreamHandler ma metodę setLevel(min), ale nie ma setLevel(max).
    Jeśli dodamy do stdout handler z setLevel(DEBUG), to ERROR też trafi na stdout,
    bo ERROR > DEBUG. Żeby tego uniknąć, dokładamy własny filtr który odcina
    wszystko powyżej WARNING – dzięki temu ERROR i CRITICAL idą TYLKO na stderr.
    """

    def __init__(self, max_level: int):
        super().__init__()
        self._max = max_level

    def filter(self, record: logging.LogRecord) -> bool:
        # zwracamy True = przepuść, False = zablokuj
        return record.levelno <= self._max


def setup_logging() -> None:
    """Konfiguruje logging zgodnie z wymaganiami zadania 6.

    Architektura: jeden logger główny (root) z poziomem DEBUG,
    dwa handlery filtrują ruch do odpowiednich strumieni:
      - h_out: DEBUG / INFO / WARNING → sys.stdout
      - h_err: ERROR / CRITICAL       → sys.stderr

    Dlaczego root.setLevel(DEBUG)? Logger główny domyślnie ma poziom WARNING,
    co blokowałoby komunikaty DEBUG i INFO zanim w ogóle trafią do handlerów.
    Ustawiamy go na DEBUG, żeby wszystko przechodziło – handlery same filtrują.
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # format: godzina [POZIOM  ] treść – wyrównanie do 8 znaków dla czytelności
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(message)s", datefmt="%H:%M:%S"
    )

    # handler stdout – przepuszcza DEBUG, INFO, WARNING; blokuje ERROR wzwyż
    h_out = logging.StreamHandler(sys.stdout)
    h_out.setLevel(logging.DEBUG)
    h_out.addFilter(_MaxLevelFilter(logging.WARNING))
    h_out.setFormatter(fmt)

    # handler stderr – odbiera tylko ERROR i CRITICAL
    h_err = logging.StreamHandler(sys.stderr)
    h_err.setLevel(logging.ERROR)
    h_err.setFormatter(fmt)

    root.addHandler(h_out)
    root.addHandler(h_err)


# __name__ to nazwa bieżącego modułu – pozwala filtrować logi wg pliku źródłowego
log = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Funkcje pomocnicze do pracy z danymi z parser.py
# ─────────────────────────────────────────────────────────────────────────────

def find_measurement_file(mdir: Path, quantity: str, frequency: str) -> Path | None:
    """Zwraca ścieżkę do pliku pomiarowego dla podanej wielkości i częstotliwości.

    Przeszukuje słownik zwrócony przez group_measurement_files_by_key.
    Porównanie wielkości jest case-insensitive – użytkownik może wpisać
    'pm10' zamiast 'PM10' i program nadal znajdzie właściwy plik.
    Zwraca None jeśli żaden plik nie pasuje – caller sam decyduje co zrobić.
    """
    for (_, q, freq), path in group_measurement_files_by_key(mdir).items():
        if q.upper() == quantity.upper() and freq == frequency:
            return path
    return None


def get_values_in_range(
    station_dict: dict,
    start: datetime,
    end: datetime,
) -> list[float]:
    """Wyodrębnia wartości pomiarowe w przedziale [start, end] dla jednej stacji.

    Struktura station_dict (zwracanego przez parse_measurement_file):
      - klucze będące napisami jak "Nr", "Kod stacji" → metadane, pomijamy je
      - klucze będące datami w formacie "DD/MM/YY HH:MM" → wartości float

    Rozróżniamy je przez isinstance(val, float) – metadane są napisami,
    pomiary są floatami. Dodatkowo try/except łapie klucze które wyglądają
    jak daty ale mają zły format.
    """
    values = []
    for key, val in station_dict.items():
        if not isinstance(val, float):
            continue  # metadane: "Kod stacji", "Wskaźnik" itp. – pomijamy
        try:
            dt = datetime.strptime(key, "%d/%m/%y %H:%M")
        except ValueError:
            continue  # klucz nie jest datą w oczekiwanym formacie
        if start <= dt <= end:
            values.append(val)
    return values


def build_mdata(measurements: list[dict]) -> dict[str, dict]:
    """Zamienia listę słowników stacji na słownik indeksowany kodem stacji.

    parse_measurement_file zwraca listę – żeby znaleźć stację po kodzie,
    trzeba by iterować całą listę za każdym razem (O(n)).
    Słownik daje dostęp w O(1), co ma znaczenie przy wielu zapytaniach.
    """
    return {s["Kod stacji"]: s for s in measurements}


# ─────────────────────────────────────────────────────────────────────────────
# Podkomendy CLI
# ─────────────────────────────────────────────────────────────────────────────

def cmd_random(args, stations: list[dict], measurements: list[dict]) -> None:
    """Wypisuje nazwę i adres losowej stacji mającej dane w zadanym przedziale.

    Logika:
      1. Budujemy indeks pomiarów (build_mdata) dla szybkiego dostępu.
      2. Zbieramy kody stacji które mają ≥1 pomiar w przedziale.
      3. Szukamy metadanych tych stacji w pliku stacje.csv.
      4. Losujemy jedną i wypisujemy jej dane.
    """
    start = datetime.fromisoformat(args.start)
    end   = datetime.fromisoformat(args.end)

    mdata = build_mdata(measurements)

    # set comprehension – zbieramy kody stacji z ≥1 pomiarem w przedziale
    active_codes = {
        code for code, sdict in mdata.items()
        if get_values_in_range(sdict, start, end)
    }

    if not active_codes:
        # WARNING bo brak danych nie jest błędem programu – to informacja dla użytkownika
        log.warning(
            "Brak pomiarów dla %s %s w przedziale %s – %s",
            args.quantity, args.frequency, args.start, args.end,
        )
        print("Brak danych dla podanych parametrów.")
        return

    # pliki pomiarowe i stacje.csv to oddzielne źródła – łączymy je przez kod stacji
    active_stations = [s for s in stations if s.get("Kod stacji") in active_codes]

    if not active_stations:
        # może się zdarzyć gdy plik pomiarowy zawiera stację nieobecną w stacje.csv
        log.warning("Kody aktywnych stacji nie znaleziono w stacje.csv: %s", active_codes)
        print("Nie znaleziono metadanych dla aktywnych stacji.")
        return

    # random.choice zwraca losowy element listy – każda stacja ma równe szanse
    s = random.choice(active_stations)
    adres = s.get("Adres") or s.get("Miejscowość", "")
    print(f"Nazwa:   {s['Nazwa stacji']}")
    print(f"Adres:   {s['Województwo']}, {s['Miejscowość']}, {adres}")


def cmd_stats(args, stations: list[dict], measurements: list[dict]) -> None:
    """Oblicza średnią arytmetyczną i odchylenie standardowe dla danej stacji.

    Odchylenie standardowe jest populacyjne (dzielimy przez N, nie N-1),
    bo analizujemy wszystkie dostępne pomiary, a nie próbkę.
    """
    start = datetime.fromisoformat(args.start)
    end   = datetime.fromisoformat(args.end)

    mdata = build_mdata(measurements)

    if args.station not in mdata:
        # stacja istnieje w stacje.csv, ale nie mierzy tej wielkości – to WARNING
        log.warning(
            "Stacja %s nie mierzy %s %s (brak w pliku pomiarowym)",
            args.station, args.quantity, args.frequency,
        )
        print(f"Stacja '{args.station}' nie ma danych dla {args.quantity} {args.frequency}.")
        return

    values = get_values_in_range(mdata[args.station], start, end)

    if not values:
        # stacja istnieje w pliku, ale nie ma pomiarów w podanym przedziale
        log.warning(
            "Brak pomiarów dla stacji %s w przedziale %s – %s",
            args.station, args.start, args.end,
        )
        print(f"Brak pomiarów dla stacji '{args.station}' w podanym przedziale.")
        return

    mean = sum(values) / len(values)

    # wzór na odchylenie standardowe populacyjne: sqrt(Σ(xi - μ)² / N)
    std = math.sqrt(sum((v - mean) ** 2 for v in values) / len(values))

    # szukamy pełnej nazwy stacji w metadanych (next z wartością domyślną = bezpieczne)
    info = next((s for s in stations if s.get("Kod stacji") == args.station), None)
    name = info["Nazwa stacji"] if info else args.station

    print(f"Stacja:       {name} ({args.station})")
    print(f"Wielkość:     {args.quantity}  |  Częstotliwość: {args.frequency}")
    print(f"Przedział:    {args.start} → {args.end}")
    print(f"Pomiary:      {len(values)}")
    print(f"Średnia:      {mean:.4f}")
    print(f"Odch. std.:   {std:.4f}")


def cmd_anomalies(args, stations: list[dict], measurements: list[dict]) -> None:
    """Wykrywa anomalie w danych pomiarowych dla zadanego okresu.

    detect_anomalies oczekuje płaskiej listy krotek (czas, wartość, stacja, wielkość).
    Musimy więc "rozwinąć" słownikową strukturę danych do tej postaci.
    """
    start = datetime.fromisoformat(args.start)
    end   = datetime.fromisoformat(args.end)

    mdata = build_mdata(measurements)

    # zamieniamy słowniki stacji w płaską listę krotek wymaganą przez detect_anomalies
    flat: list[tuple] = []
    for code, sdict in mdata.items():
        if args.station and code != args.station:
            continue  # opcjonalne ograniczenie do jednej stacji
        for key, val in sdict.items():
            if not isinstance(val, float):
                continue  # pomijamy metadane
            try:
                dt = datetime.strptime(key, "%d/%m/%y %H:%M")
            except ValueError:
                continue
            if start <= dt <= end:
                flat.append((dt, val, code, args.quantity))

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

    # budujemy słownik nazw raz, żeby nie szukać w pętli za każdą anomalią
    station_names = {s["Kod stacji"]: s["Nazwa stacji"] for s in stations}
    print(f"Wykryto {len(anomalies)} anomalii:\n")
    for a in anomalies:
        name = station_names.get(a["station"], a["station"])
        # :10s – wyrównanie typu do 10 znaków dla czytelności kolumn
        print(f"  [{a['type'].upper():10s}] {name}  {a['detail']}")


# ─────────────────────────────────────────────────────────────────────────────
# Walidacja argumentów (zad. 5c)
# ─────────────────────────────────────────────────────────────────────────────

def _valid_date(value: str) -> str:
    """Waliduje datę wpisaną przez użytkownika.

    argparse wywołuje tę funkcję automatycznie dla argumentów z type=_valid_date.
    Jeśli format jest nieprawidłowy, rzucamy ArgumentTypeError – argparse sam
    wypisze czytelny komunikat błędu i zakończy program z kodem 2.
    strptime z "%Y-%m-%d" odrzuca np. 2023-13-01 (miesiąc 13) co chroni
    przed przekazaniem nieprawidłowej daty do filtrowania pomiarów.
    """
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value  # zwracamy napis – konwersję do datetime robimy później
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Nieprawidłowa data '{value}' – oczekiwany format: RRRR-MM-DD"
        )


def _valid_quantity(value: str) -> str:
    """Waliduje nazwę wielkości mierzonej.

    fullmatch wymaga dopasowania CAŁEGO napisu (inaczej niż match/search).
    Wzorzec [\w.()\-]+ dopuszcza: litery, cyfry, podkreślnik (z \w),
    kropkę (dla PM2.5), nawiasy (dla As(PM10)) i myślnik.
    Spacje, cudzysłowy itp. są odrzucane.
    """
    if not re.fullmatch(r"[\w.()\-]+", value):
        raise argparse.ArgumentTypeError(
            f"Nieprawidłowa wielkość '{value}' – użyj np. PM10, PM2.5, NO2, C6H6"
        )
    return value


def _valid_frequency(value: str) -> str:
    """Waliduje częstotliwość – akceptuje tylko '1g' i '24g'."""
    if value not in ("1g", "24g"):
        raise argparse.ArgumentTypeError(
            f"Nieprawidłowa częstotliwość '{value}' – użyj 1g lub 24g"
        )
    return value


# ─────────────────────────────────────────────────────────────────────────────
# Budowanie parsera CLI (zad. 5)
# ─────────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """Tworzy parser z argumentami globalnymi i trzema podkomendami.

    Argumenty globalne (--quantity, --frequency, --start, --end) są wymagane
    dla każdej podkomendy – definiujemy je raz na poziomie głównego parsera.
    Podkomendy tworzone przez add_subparsers mogą mieć własne dodatkowe argumenty
    (np. --station dla 'stats').
    """
    parser = argparse.ArgumentParser(
        prog="task5.py",
        description="Analizator danych pomiarowych jakości powietrza (dane GIOŚ).",
        # RawDescriptionHelpFormatter zachowuje formatowanie epiloga (wcięcia, nowe linie)
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

    # dest="command" – po sparsowaniu args.command będzie miało wartość "random"/"stats"/"anomalies"
    sub = parser.add_subparsers(dest="command", required=True, title="podkomendy")

    sub.add_parser(
        "random",
        help="Wypisuje nazwę i adres losowej stacji mierzącej daną wielkość w przedziale",
    )

    sp_stats = sub.add_parser(
        "stats",
        help="Oblicza średnią i odchylenie standardowe dla wskazanej stacji",
    )
    sp_stats.add_argument(
        "--station", required=True, metavar="KOD",
        help="Kod stacji pomiarowej, np. DsWrocWybCon",
    )

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
        help=f"Maks. skok między kolejnymi pomiarami (domyślnie: {DEFAULT_DELTA})",
    )
    # dest="bad_ratio" bo argparse zamienia myślnik na podkreślnik tylko w dest, nie w args
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

    if not stations_file.exists():
        # brak pliku = błąd krytyczny, dalsze działanie niemożliwe → ERROR + exit(1)
        log.error("Nie znaleziono pliku stacji: %s", stations_file)
        sys.exit(1)
    if not meas_dir.is_dir():
        log.error("Nie znaleziono katalogu z pomiarami: %s", meas_dir)
        sys.exit(1)

    stations  = parse_stations(stations_file)
    meas_file = find_measurement_file(meas_dir, args.quantity, args.frequency)

    if meas_file is None:
        # brak pliku to nie błąd aplikacji – może użytkownik wpisał nieobsługiwaną wielkość
        log.warning(
            "Brak pliku pomiarowego dla wielkości='%s' częstotliwość='%s' w %s",
            args.quantity, args.frequency, meas_dir,
        )
        print(f"Brak pliku danych dla '{args.quantity}' z częstotliwością '{args.frequency}'.")
        sys.exit(0)

    measurements = parse_measurement_file(meas_file)

    # dispatch zamiast if/elif – żeby dodać nową podkomendę wystarczy dopisać jeden wpis
    dispatch = {
        "random":    cmd_random,
        "stats":     cmd_stats,
        "anomalies": cmd_anomalies,
    }
    dispatch[args.command](args, stations, measurements)


if __name__ == "__main__":
    main()
