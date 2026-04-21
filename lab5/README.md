# Laboratorium 5 – Wyrażenia regularne, interfejsy linii komend

## Struktura plików

| Plik | Zadanie | Opis |
|---|---|---|
| `task1.py` | Zad. 1 | Funkcje parsujące `stacje.csv` i pliki pomiarowe |
| `task2.py` | Zad. 2 | `group_measurement_files_by_key` – grupowanie plików regex'em |
| `task3.py` | Zad. 3 | `get_addresses` – wydobywanie adresów stacji dla danego miasta |
| `task4.py` | Zad. 4 | Zadania a–g na wyrażeniach regularnych |
| `task5.py` | Zad. 5 & 6 | CLI z `argparse` + moduł `logging` |
| `task_ext1.py` | Zad. rozszerz. 1 | CLI z `click` – ten sam projekt co zad. 5 |
| `task_ext2.py` | Zad. rozszerz. 2 | Funkcja `detect_anomalies` – wykrywanie anomalii |

Dane wejściowe umieszczone w katalogu `data/`:

```
data/
├── stacje.csv
└── measurements/
    ├── 2023_NO_1g.csv
    ├── 2023_PM10_24g.csv
    └── ...
```

---

## Zadanie 5 & 6 – CLI (`task5.py`)

Program analizuje dane pomiarowe jakości powietrza ze stacji GIOŚ.

### Argumenty globalne

| Argument | Opis | Przykład |
|---|---|---|
| `--quantity` | Mierzona wielkość | `PM10`, `NO`, `SO2`, `C6H6` |
| `--frequency` | Częstotliwość pomiaru | `1g` (godzinowa) lub `24g` (dobowa) |
| `--start` | Początek przedziału | `2023-01-01` |
| `--end` | Koniec przedziału | `2023-12-31` |
| `--data-dir` | Katalog z danymi | `data/` (domyślnie) |

### Podkomendy

#### `random` – losowa stacja

Wypisuje nazwę i adres losowej stacji, która posiadała pomiary danej wielkości
w zadanym przedziale czasowym.

```bash
python task5.py --quantity NO --frequency 1g --start 2023-01-01 --end 2023-01-31 random
```

Przykładowy wynik:

```
Nazwa:   Wrocław, wyb. Conrada-Korzeniowskiego
Adres:   DOLNOŚLĄSKIE, Wrocław, Wyb. J.Conrada-Korzeniowskiego
```

---

#### `stats` – statystyki dla stacji

Oblicza średnią arytmetyczną i odchylenie standardowe dla wskazanej stacji
w zadanym przedziale.

```bash
python task5.py --quantity PM10 --frequency 24g \
    --start 2023-06-01 --end 2023-06-30 \
    stats --station DsWrocWybCon
```

Przykładowy wynik:

```
Stacja:       Wrocław, wyb. Conrada-Korzeniowskiego (DsWrocWybCon)
Wielkość:     PM10  |  Częstotliwość: 24g
Przedział:    2023-06-01 → 2023-06-30
Pomiary:      12
Średnia:      24.7333
Odch. std.:   15.1569
```

---

#### `anomalies` – wykrywanie anomalii (zad. rozszerz. 2)

Wykrywa podejrzane serie pomiarów. Szczegóły w sekcji [Zadanie rozszerzające 2](#zadanie-rozszerzające-2--wykrywanie-anomalii-task_ext2py).

```bash
python task5.py --quantity NO --frequency 1g \
    --start 2023-01-01 --end 2023-12-31 \
    anomalies --delta 50
```

### Walidacja

Program waliduje:
- **format daty** – musi być `RRRR-MM-DD`; nieprawidłowa data kończy program z komunikatem błędu
- **format wielkości** – musi zawierać tylko litery, cyfry, nawiasy i kropki (np. `PM2.5`, `C6H6`)
- **częstotliwość** – tylko `1g` lub `24g`

### Logging (zad. 6)

| Poziom | Gdzie | Kiedy |
|---|---|---|
| `DEBUG` | stdout | po każdym odczytanym wierszu – liczba bajtów |
| `INFO` | stdout | otwarcie i zamknięcie każdego pliku |
| `WARNING` | stdout | brak danych dla parametrów, nieobsługiwana stacja |
| `ERROR` | **stderr** | brak pliku / katalogu – program kończy działanie |

Aby ukryć logi DEBUG i INFO podczas normalnego użycia:

```bash
python task5.py ... 2>/dev/null | grep -v '^\d\d:\d\d'
# lub przekieruj stdout do pliku logów:
python task5.py ... > run.log 2>errors.log
```

---

## Zadanie rozszerzające 1 – CLI z Click (`task_ext1.py`)

Identyczna funkcjonalność co `task5.py`, zbudowana z użyciem biblioteki
[Click](https://click.palletsprojects.com/).

### Instalacja

```bash
pip install click
```

### Użycie

Składnia różni się od `task5.py`: opcje podajemy **po** nazwie podkomendy.

```bash
python task_ext1.py random    --quantity NO   --frequency 1g  --start 2023-01-01 --end 2023-01-31
python task_ext1.py stats     --quantity PM10 --frequency 24g --start 2023-06-01 --end 2023-06-30 --station DsWrocWybCon
python task_ext1.py anomalies --quantity NO   --frequency 1g  --start 2023-01-01 --end 2023-12-31 --delta 50
```

### Porównanie argparse vs Click

| Cecha | `argparse` (zad. 5) | `click` (zad. rozszerz. 1) |
|---|---|---|
| Deklaracja opcji | `parser.add_argument(...)` na obiekcie parsera | dekorator `@click.option(...)` nad funkcją |
| Walidacja dozwolonych wartości | ręczna funkcja `type=` | `click.Choice([...])` |
| Opis komendy | `help=` w `add_parser` | docstring funkcji |
| Wspólne opcje | powtórzenie lub `parents=` | dekorator wielokrotnego użytku |
| Kolejność opcji | globalne **przed** podkomendą | opcje **po** podkomendzie |
| Komunikaty błędów | plain text | kolorowane w terminalu |
| Testowalność | wymaga mockowania `sys.argv` | wbudowany `CliRunner` |

---

## Zadanie rozszerzające 2 – Wykrywanie anomalii (`task_ext2.py`)

Funkcja `detect_anomalies` analizuje serię pomiarów i zwraca listę wykrytych
nieprawidłowości według trzech reguł:

### Reguły detekcji

| Typ | Nazwa | Opis |
|---|---|---|
| `bad_data` | Złe dane | Udział wartości `None` / zerowych / ujemnych przekracza próg (domyślnie 30%) |
| `jump` | Nagły skok | Różnica między kolejnymi pomiarami przekracza próg (domyślnie 200 µg/m³) |
| `spike` | Przekroczenie progu | Pojedynczy pomiar przekracza wartość alarmową dla danej wielkości |

### Progi alarmowe

| Wielkość | Próg (µg/m³) |
|---|---|
| PM10 | 500 |
| PM2.5 | 300 |
| NO2 | 400 |
| SO2 | 500 |
| O3 | 400 |
| CO | 30 000 |
| inne | 1 000 |

### Podkomenda `anomalies`

Dostępna w obu CLI (`task5.py` i `task_ext1.py`):

```bash
# wszystkie stacje, próg skoku = 50
python task5.py --quantity NO --frequency 1g \
    --start 2023-01-01 --end 2023-12-31 \
    anomalies --delta 50

# jedna stacja, własny próg złych danych
python task5.py --quantity PM10 --frequency 24g \
    --start 2023-01-01 --end 2023-12-31 \
    anomalies --station DsWrocWybCon --bad-ratio 0.1
```

Przykładowy wynik:

```
Wykryto 4 anomalii:

  [JUMP      ] Szczecin, ul. Piłsudskiego  Δ=51.65 między 2023-12-12 03:00:00 a 2023-12-12 03:00:00 (1.44 → 53.09)
  [JUMP      ] Widuchowa  Δ=56.14 między 2023-01-03 06:00:00 a 2023-01-03 07:00:00 (0.30 → 56.44)
  [BAD_DATA  ] Kraków, ul. Bujaka  45/150 wartości to None/zero/ujemne (30%)
  [SPIKE     ] Warszawa, ul. Kondratowicza  512.30 > 500 o 2023-03-15 14:00:00
```

---

## Szybki start

```bash
# sklonuj repozytorium i wejdź do katalogu lab5
cd lab5

# zainstaluj click (tylko do task_ext1.py)
pip install click

# losowa stacja dla NO, pomiary godzinowe, styczeń 2023
python task5.py --quantity NO --frequency 1g --start 2023-01-01 --end 2023-01-31 random

# statystyki PM10 dobowe dla konkretnej stacji
python task5.py --quantity PM10 --frequency 24g --start 2023-01-01 --end 2023-12-31 stats --station DsWrocWybCon

# anomalie z niskim progiem skoku (Click)
python task_ext1.py anomalies --quantity NO --frequency 1g --start 2023-01-01 --end 2023-12-31 --delta 50
```
