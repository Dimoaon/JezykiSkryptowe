# Laboratorium 4 – Zadania 1, 2, 3

## Zadanie 1 – Zmienne środowiskowe (`env.py`)

Skrypt wyświetla wszystkie zmienne środowiskowe w porządku alfabetycznym.
Opcjonalnie przyjmuje dowolną liczbę argumentów linii komend – filtruje wtedy zmienne, których nazwy zawierają podany ciąg znaków (filtr działa case-insensitive).

### Użycie

```bash
# Wyświetl wszystkie zmienne środowiskowe
python env.py

# Filtruj zmienne zawierające "path" w nazwie
python env.py path

# Filtruj po kilku frazach jednocześnie
python env.py path home user
```

### Przykładowy wynik

```
PATH=/usr/bin:/usr/local/bin
```

---

## Zadanie 2 – Zmienna PATH (`path.py`)

Skrypt operuje na zmiennej środowiskowej `PATH`.

### Użycie

```bash
# Wypisz wszystkie katalogi z PATH
python path.py --list

# Wypisz katalogi wraz z plikami wykonywalnymi
python path.py --executables
```

### Przykładowy wynik

```
# --list
/usr/bin
/usr/local/bin

# --executables
/usr/bin:
  cat
  ls
  python3
```

---

## Zadanie 3 – Własna wersja `tail` (`tail.py`)

Skrypt wypisuje ostatnie N linii pliku lub danych ze standardowego wejścia.

### Użycie

```bash
# Ostatnie 10 linii z pliku (domyślnie)
python tail.py plik.txt

# Ostatnie 5 linii z pliku
python tail.py --lines=5 plik.txt

# Dane ze standardowego wejścia
cat plik.txt | python tail.py

# Gdy podano i plik i stdin – plik ma pierwszeństwo
cat plik.txt | python tail.py inny_plik.txt

# Tryb follow – czeka na nowe linie w pliku (jak tail -f)
python tail.py --follow plik.txt

# Kombinacja
python tail.py --lines=5 --follow plik.txt
```

### Parametry

| Parametr | Opis | Domyślnie |
|---|---|---|
| `--lines=N` | Liczba ostatnich linii do wypisania | `10` |
| `--follow` | Czeka na nowe linie w pliku po wypisaniu | wyłączone |
| `plik` | Ścieżka do pliku (opcjonalnie) | stdin |
