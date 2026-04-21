"""
Zadanie rozszerzające 1 – CLI zbudowane z użyciem biblioteki Click.

Click vs argparse – główne różnice:
  - Argumenty i opcje deklaruje się dekoratorami (@click.option) bezpośrednio
    nad funkcją komendy, zamiast budować parser obiektowo.
  - Wspólne opcje można zgrupować w dekoratorze wielokrotnego użytku (patrz: common_options).
  - click.Choice zastępuje ręczną walidację dozwolonych wartości (częstotliwość).
  - Opis komendy pochodzi automatycznie z docstringa funkcji.
  - Kluczna różnica w kolejności argumentów:
      argparse:  task5.py      --quantity NO --frequency 1g ... random
      click:     task_ext1.py  random --quantity NO --frequency 1g ...
    W Click opcje należą do podkomendy, więc muszą pojawić się po jej nazwie.
  - Komunikaty błędów są kolorowane w terminalu (Click używa styled output).

Uruchomienie:
  python task_ext1.py random   --quantity NO  --frequency 1g  --start 2023-01-01 --end 2023-01-31
  python task_ext1.py stats    --quantity PM10 --frequency 24g --start 2023-06-01 --end 2023-06-30 --station DsWrocWybCon
  python task_ext1.py anomalies --quantity NO --frequency 1g  --start 2023-01-01 --end 2023-12-31 --delta 50
"""

import logging
import sys
from pathlib import Path

import click

# importujemy logikę biznesową z task5.py i pomocnicze stałe z task_ext2.py
from task1 import parse_stations, parse_measurements
from task2 import group_measurement_files_by_key
from task5 import (
    cmd_anomalies, cmd_random, cmd_stats,
    find_measurement_file, setup_logging,
)
from task_ext2 import DEFAULT_BAD_RATIO, DEFAULT_DELTA

log = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Własne typy parametrów Click (odpowiednik type= w argparse)
# ─────────────────────────────────────────────────────────────────────────────

class _DateType(click.ParamType):
    """Waliduje datę w formacie RRRR-MM-DD i zwraca ją jako napis."""
    name = "RRRR-MM-DD"

    def convert(self, value, param, ctx):
        from datetime import datetime
        if isinstance(value, str):
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return value
            except ValueError:
                # self.fail rzuca UsageError – Click sam formatuje komunikat błędu
                self.fail(
                    f"Nieprawidłowa data '{value}' – oczekiwany format: RRRR-MM-DD",
                    param, ctx,
                )
        return value


class _QuantityType(click.ParamType):
    """Sprawdza, czy wielkość mierzona zawiera tylko dozwolone znaki."""
    name = "WIELKOŚĆ"

    def convert(self, value, param, ctx):
        import re
        if not re.fullmatch(r"[\w.()\-]+", value):
            self.fail(
                f"Nieprawidłowa wielkość '{value}' – użyj np. PM10, NO2, C6H6",
                param, ctx,
            )
        return value


_DATE     = _DateType()
_QUANTITY = _QuantityType()


# ─────────────────────────────────────────────────────────────────────────────
# Dekorator ze wspólnymi opcjami
# ─────────────────────────────────────────────────────────────────────────────

def common_options(f):
    """Dokłada do komendy pięć opcji wspólnych dla wszystkich podkomend.

    Używamy reversed(), bo dekoratory nakładają się od dołu – bez odwrócenia
    kolejność opcji w --help byłaby odwrócona względem deklaracji.
    """
    for decorator in reversed([
        click.option(
            "--data-dir",
            type=click.Path(file_okay=False, path_type=Path),
            default="data", show_default=True,
            help="Katalog z plikami stacje.csv i measurements/",
        ),
        click.option(
            "--quantity", required=True, type=_QUANTITY,
            help="Mierzona wielkość, np. PM10, NO, SO2",
        ),
        click.option(
            "--frequency", required=True,
            type=click.Choice(["1g", "24g"]),  # Click sam generuje komunikat o dozwolonych wartościach
            metavar="CZĘST.",
            help="Częstotliwość pomiaru: 1g lub 24g",
        ),
        click.option(
            "--start", required=True, type=_DATE, metavar="RRRR-MM-DD",
            help="Początek przedziału (włącznie)",
        ),
        click.option(
            "--end", required=True, type=_DATE, metavar="RRRR-MM-DD",
            help="Koniec przedziału (włącznie)",
        ),
    ]):
        f = decorator(f)
    return f


# ─────────────────────────────────────────────────────────────────────────────
# Pomocnicze – ładowanie danych i namiastka Namespace
# ─────────────────────────────────────────────────────────────────────────────

class _NS:
    """Minimalna imitacja argparse.Namespace.

    Pozwala ponownie użyć funkcji cmd_* z task5.py bez ich przepisywania.
    Zwraca None dla brakujących atrybutów zamiast rzucać AttributeError.
    """

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __getattr__(self, item):
        return None


def _load(data_dir: Path, quantity: str, frequency: str):
    """Wczytuje metadane stacji i plik pomiarowy; kończy program w razie błędu."""
    stations_file = data_dir / "stacje.csv"
    meas_dir      = data_dir / "measurements"

    if not stations_file.exists():
        log.error("Nie znaleziono pliku stacji: %s", stations_file)
        sys.exit(1)
    if not meas_dir.is_dir():
        log.error("Nie znaleziono katalogu z pomiarami: %s", meas_dir)
        sys.exit(1)

    stations  = parse_stations(stations_file)
    meas_file = find_measurement_file(meas_dir, quantity, frequency)

    if meas_file is None:
        log.warning(
            "Brak pliku pomiarowego dla wielkości='%s' częstotliwość='%s'",
            quantity, frequency,
        )
        print(f"Brak pliku danych dla '{quantity}' z częstotliwością '{frequency}'.")
        sys.exit(0)

    return parse_measurements(meas_file), stations


# ─────────────────────────────────────────────────────────────────────────────
# Grupa główna
# ─────────────────────────────────────────────────────────────────────────────

@click.group()
def cli():
    """Analizator danych pomiarowych jakości powietrza (wersja Click)."""
    setup_logging()


# ─────────────────────────────────────────────────────────────────────────────
# Podkomendy
# ─────────────────────────────────────────────────────────────────────────────

@cli.command("random")
@common_options
def cmd_random_click(data_dir, quantity, frequency, start, end):
    """Wypisuje nazwę i adres losowej stacji z danymi w zadanym przedziale."""
    mdata, stations = _load(data_dir, quantity, frequency)
    cmd_random(
        _NS(quantity=quantity, frequency=frequency, start=start, end=end),
        stations, mdata,
    )


@cli.command("stats")
@common_options
@click.option(
    "--station", required=True, metavar="KOD",
    help="Kod stacji pomiarowej, np. DsWrocWybCon",
)
def cmd_stats_click(data_dir, quantity, frequency, start, end, station):
    """Oblicza średnią i odchylenie standardowe dla wskazanej stacji."""
    mdata, stations = _load(data_dir, quantity, frequency)
    cmd_stats(
        _NS(quantity=quantity, frequency=frequency,
            start=start, end=end, station=station),
        stations, mdata,
    )


@cli.command("anomalies")
@common_options
@click.option(
    "--station", default=None, metavar="KOD",
    help="Ogranicz analizę do jednej stacji (domyślnie: wszystkie)",
)
@click.option(
    "--delta", type=float, default=DEFAULT_DELTA, show_default=True,
    help="Maksymalny dozwolony skok między kolejnymi pomiarami",
)
@click.option(
    "--bad-ratio", type=float, default=DEFAULT_BAD_RATIO, show_default=True,
    help="Maks. udział wartości None/zero/ujemnych",
)
def cmd_anomalies_click(data_dir, quantity, frequency, start, end,
                        station, delta, bad_ratio):
    """Wykrywa anomalie w danych pomiarowych (złe dane, skoki, przekroczenia)."""
    mdata, stations = _load(data_dir, quantity, frequency)
    cmd_anomalies(
        _NS(quantity=quantity, frequency=frequency,
            start=start, end=end, station=station,
            delta=delta, bad_ratio=bad_ratio),
        stations, mdata,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Punkt wejściowy
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli()
