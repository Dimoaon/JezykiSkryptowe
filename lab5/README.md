# Laboratorium 5 – Wyrażenia regularne, interfejsy linii komend

## Struktura plików

| Plik | Zadanie | Opis |
|---|---|---|
| `parser.py` | Zad. 1 | `parse_stations` i `parse_measurement_file` – odczyt CSV modułem `csv` |
| `group_measurement_files_by_key.py` | Zad. 2 | Grupowanie plików pomiarowych za pomocą wyrażeń regularnych |
| `get_addresses.py` | Zad. 3 | `get_addresses` – wydobywanie adresów stacji dla danego miasta |
| `tasks.py` | Zad. 4 | Podzadania a–g z użyciem wyrażeń regularnych |
| `task5.py` | Zad. 5 & 6 | CLI z `argparse` + moduł `logging` |
| `task_ext1.py` | Zad. rozszerz. 1 | CLI z `click` – ten sam projekt co zad. 5 |
| `task_ext2.py` | Zad. rozszerz. 2 | `detect_anomalies` – wykrywanie anomalii w pomiarach |

Dane wejściowe w katalogu `data/`:

```
data/
├── stacje.csv
└── measurements/
    ├── 2023_NO_1g.csv
    ├── 2023_PM10_24g.csv
    └── ...
```

---

## Zadanie 1 – Parsowanie (`parser.py`)

Dwie funkcje parsujące pliki CSV:

- **`parse_stations(path)`** – czyta `stacje.csv`, zwraca listę słowników (jeden słownik = jedna stacja, klucze = nazwy kolumn).
- **`parse_measurement_file(path)`** – czyta plik pomiarowy, zwraca listę słowników (jeden słownik = jedna stacja z metadanymi + pomiary jako klucze dat).

Obie funkcje logują otwarcie/zamknięcie pliku (INFO) oraz rozmiar każdego wiersza (DEBUG) – wymagane przez zadanie 6.

```bash
python parser.py
```

---

## Zadanie 2 – Grupowanie plików (`group_measurement_files_by_key.py`)

Funkcja `group_measurement_files_by_key(path)` przeszukuje katalog i dopasowuje pliki wyrażeniem regularnym `^(\d{4})_(.+)_(1g|24g|1m)\.csv$`.

Zwraca słownik `{(rok, wielkość, częstotliwość): Path}`.

```bash
python group_measurement_files_by_key.py data/measurements
```

Przykładowy wynik:

```
('2023', 'NO', '1g') -> 2023_NO_1g.csv
('2023', 'PM10', '24g') -> 2023_PM10_24g.csv
```

---

## Zadanie 3 – Adresy stacji (`get_addresses.py`)

Funkcja `get_addresses(path, city)` zwraca listę czwórek `(województwo, miasto, ulica, numer)` dla stacji w podanym mieście.

Ulica i numer wyodrębniane są z kolumny `Adres` za pomocą wyrażenia regularnego – obsługuje prefiksy `ul.`/`al.`, adresy bez numeru i różne formaty numerów (`35`, `2a`, `14/16`).

```bash
python get_addresses.py data/stacje.csv Wrocław
python get_addresses.py data/stacje.csv Kraków
```

---

## Zadanie 4 – Zadania na wyrażeniach regularnych (`tasks.py`)

| Funkcja | Podzadanie | Opis |
|---|---|---|
| `extract_dates` | a | Daty `RRRR-MM-DD` z kolumn `Data uruchomienia` i `Data zamknięcia` |
| `extract_coordinates` | b | Pary `(szerokość, długość)` z 6 cyframi po kropce |
| `stations_with_dash` | c | Nazwy stacji z dokładnie jednym ` - ` (dwie części) |
| `normalize_station_names` | d | Zamiana spacji na `_` i polskich znaków na łacińskie |
| `check_mob_stations` | e | Weryfikacja czy stacje kończące się na `MOB` mają rodzaj `mobilna` |
| `locations_three_parts` | f | Nazwy stacji złożone z 3 części oddzielonych ` - ` |
| `locations_with_street` | g | Adresy zawierające przecinek i `ul.` lub `al.` |

```bash
python tasks.py
```

---

## Zadanie 5 & 6 – CLI (`task5.py`)

Program analizuje dane pomiarowe jakości powietrza GIOŚ.

### Argumenty globalne (wymagane)

| Argument | Opis | Przykład |
|---|---|---|
| `--quantity` | Mierzona wielkość | `PM10`, `NO`, `SO2`, `C6H6` |
| `--frequency` | Częstotliwość | `1g` (godzinowa) lub `24g` (dobowa) |
| `--start` | Początek przedziału | `2023-01-01` |
| `--end` | Koniec przedziału | `2023-12-31` |
| `--data-dir` | Katalog z danymi | `data/` (domyślnie) |

### Podkomenda `random`

Wypisuje nazwę i adres losowej stacji z pomiarami danej wielkości w zadanym przedziale.

```bash
python task5.py --quantity NO --frequency 1g --start 2023-01-01 --end 2023-01-31 random
```

```
Nazwa:   Wrocław, wyb. Conrada-Korzeniowskiego
Adres:   DOLNOŚLĄSKIE, Wrocław, Wyb. J.Conrada-Korzeniowskiego
```

### Podkomenda `stats`

Oblicza średnią i odchylenie standardowe dla wskazanej stacji.

```bash
python task5.py --quantity PM10 --frequency 24g \
    --start 2023-06-01 --end 2023-06-30 \
    stats --station DsWrocWybCon
```

```
Stacja:       Wrocław, wyb. Conrada-Korzeniowskiego (DsWrocWybCon)
Wielkość:     PM10  |  Częstotliwość: 24g
Przedział:    2023-06-01 → 2023-06-30
Pomiary:      12
Średnia:      24.7333
Odch. std.:   15.1569
```

### Podkomenda `anomalies` (zad. rozszerz. 2)

```bash
python task5.py --quantity NO --frequency 1g \
    --start 2023-01-01 --end 2023-12-31 \
    anomalies --delta 50
```

### Walidacja wejścia (zad. 5c)

Program odrzuca nieprawidłowe argumenty z czytelnym komunikatem:

```bash
python task5.py --quantity NO --frequency 5h --start 2023-13-01 --end 2023-01-31 random
# error: Nieprawidłowa częstotliwość '5h' – użyj 1g lub 24g
# error: Nieprawidłowa data '2023-13-01' – oczekiwany format: RRRR-MM-DD
```

### Logging (zad. 6)

| Poziom | Gdzie | Kiedy |
|---|---|---|
| `DEBUG` | stdout | rozmiar każdego odczytanego wiersza w bajtach |
| `INFO` | stdout | otwarcie i zamknięcie każdego pliku CSV |
| `WARNING` | stdout | brak danych dla parametrów, stacja nie mierzy danej wielkości |
| `ERROR` | **stderr** | brak pliku stacji lub katalogu pomiarów |

---

## Zadanie rozszerzające 1 – CLI z Click (`task_ext1.py`)

Identyczna funkcjonalność co `task5.py`, zbudowana z użyciem biblioteki [Click](https://click.palletsprojects.com/).

```bash
pip install click
```

**Kluczowa różnica w składni:** opcje podajemy **po** nazwie podkomendy.

```bash
# argparse (task5.py) – opcje PRZED podkomendą
python task5.py --quantity NO --frequency 1g --start 2023-01-01 --end 2023-01-31 random

# click (task_ext1.py) – opcje PO podkomendzie
python task_ext1.py random --quantity NO --frequency 1g --start 2023-01-01 --end 2023-01-31
```

### Porównanie argparse vs Click

| Cecha | `argparse` | `click` |
|---|---|---|
| Deklaracja opcji | `parser.add_argument(...)` | dekorator `@click.option(...)` |
| Walidacja wartości | ręczna funkcja `type=` | `click.Choice([...])` |
| Opis komendy | `help=` w `add_parser()` | docstring funkcji |
| Wspólne opcje | `parents=` lub powtórzenie | dekorator wielokrotnego użytku |
| Kolejność opcji | globalne **przed** podkomendą | opcje **po** podkomendzie |
| Komunikaty błędów | plain text | kolorowane w terminalu |
| Testowanie | mock `sys.argv` | wbudowany `CliRunner` |

---

## Zadanie rozszerzające 2 – Wykrywanie anomalii (`task_ext2.py`)

Funkcja `detect_anomalies(measurements, ...)` analizuje listę krotek `(czas, wartość, stacja, wielkość)` i wykrywa trzy typy anomalii:

| Typ | Opis | Domyślny próg |
|---|---|---|
| `BAD_DATA` | Zbyt duży udział wartości `None`/zerowych/ujemnych | 30% |
| `JUMP` | Nagły skok między kolejnymi pomiarami | 200 µg/m³ |
| `SPIKE` | Przekroczenie progu alarmowego dla danej wielkości | PM10: 500, PM2.5: 300, ... |

Dostępna jako podkomenda `anomalies` w obu CLI:

```bash
# wszystkie stacje, obniżony próg skoku
python task5.py --quantity NO --frequency 1g --start 2023-01-01 --end 2023-12-31 anomalies --delta 50

# jedna stacja
python task5.py --quantity PM10 --frequency 24g --start 2023-01-01 --end 2023-12-31 \
    anomalies --station DsWrocWybCon --bad-ratio 0.1

# to samo przez Click
python task_ext1.py anomalies --quantity NO --frequency 1g --start 2023-01-01 --end 2023-12-31 --delta 50
```

Przykładowy wynik:

```
Wykryto 4 anomalii:

  [JUMP      ] Widuchowa  Δ=56.14 między 2023-01-03 06:00:00 a 2023-01-03 07:00:00 (0.30 → 56.44)
  [BAD_DATA  ] Kraków, ul. Bujaka  45/150 wartości to None/zero/ujemne (30%)
```

---

## Szybki start

```bash
cd lab5

# zainstaluj click (tylko task_ext1.py)
pip install click

# losowa stacja dla NO godzinowego, styczeń 2023
python task5.py --quantity NO --frequency 1g --start 2023-01-01 --end 2023-01-31 random

# statystyki PM10 dobowego dla konkretnej stacji, cały 2023
python task5.py --quantity PM10 --frequency 24g --start 2023-01-01 --end 2023-12-31 stats --station DsWrocWybCon

# anomalie NO z obniżonym progiem skoku (wersja Click)
python task_ext1.py anomalies --quantity NO --frequency 1g --start 2023-01-01 --end 2023-12-31 --delta 50
```
