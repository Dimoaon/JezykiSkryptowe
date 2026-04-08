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

---

## Zadanie 4 – Analiza plików tekstowych (`analyzer.py`, `runner.py`)

Program analizuje pliki tekstowe pod kątem statystycznym.

Pierwszy skrypt (`analyzer.py`) czyta ścieżkę do pliku
ze standardowego wejścia i zwraca statystyki w formacie JSON.

Drugi skrypt (`runner.py`) uruchamia analizę dla wszystkich plików
w katalogu, wykorzystując `subprocess`, a następnie agreguje wyniki.

### Użycie

```bash
# Analiza pojedynczego pliku (stdin)
echo "plik.txt" | python analyzer.py

# Analiza wszystkich plików w katalogu
python runner.py folder
```

### Przykładowy wynik

```
{
    "files_processed": 3,
    "total_chars": 1200,
    "total_words": 200,
    "total_lines": 50,
    "most_common_char": "a",
    "most_common_word": "the"
}
```

---

## Zadanie 5 – Konwersja multimediów (`mediaconvert.py`, `utils.py`)

Skrypt konwertuje pliki multimedialne (audio, wideo oraz obrazy) do wybranego formatu.

Wykorzystuje:

* `ffmpeg` dla audio/wideo
* `ImageMagick` (`magick`) dla obrazów

Obsługuje zmienną środowiskową `CONVERTED_DIR` oraz zapisuje historię konwersji.

### Użycie

```bash
# Konwersja plików do formatu mp4
python mediaconvert.py folder mp4
```

### Zmienna środowiskowa

```bash
# Linux / Mac
export CONVERTED_DIR=./output

# Windows
set CONVERTED_DIR=output
```

### Przykładowy wynik

```
Converted: video.avi -> converted/20260408-142530-video.mp4
```

### Historia konwersji

Zapisywana w pliku `history.json`:

```
{
    "timestamp": "2026-04-08T14:25:30",
    "input_path": "video.avi",
    "output_format": "mp4",
    "output_path": "converted/20260408-142530-video.mp4",
    "program": "ffmpeg"
}
```
