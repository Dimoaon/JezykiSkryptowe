# Lab 2 - Text Processing

## Opis
Program czyta dane ze standardowego wejscia i wypisuje tylko tresc ksiazki:
- bez preambuly,
- bez informacji o wydaniu po linii `-----`,
- z zachowaniem struktury akapitow,
- po usunieciu zbednych spacji na poczatku i koncu linii
  oraz nadmiarowych bialych znakow wewnatrz linii.

---

## Struktura

```
lab2/
├── core/
│   ├── cleaner.py
│   ├── parser.py
│   └── utils.py
├── data/
├── lab_2.py
└── README.md
```

---

## Uruchomienie

Z folderu `lab2`:

```
python lab_2.py < data/krolowa_sniegu.txt
python lab_2.py < data/dziewczynka_z_zapalkami.txt
python lab_2.py < data/ojciec_goriot.txt
```

---

## Jak działa

- `cleaner.py` - czyta dane potokowo i usuwa preambule oraz informacje o wydaniu
- `parser.py` - dzieli tekst na zdania i jest przygotowany pod dalsze funkcjonalnosci
- `utils.py` - miejsce na kolejne funkcje przetwarzajace zdania

Parser wywoluje funkcje dla kazdego zdania:

```
process_sentences(text, process_function)
```

---

## Podział pracy

### Dzmitry Skavarodka
- cleaner
- parser
- przetwarzanie potokowe stdin -> stdout
- struktura projektu
- pipeline (stdin → output)

### Szymon Majerczak
Do zrobienia w `utils.py`:
- count_words()
- average_sentence_length()
- longest_sentence()

Przykład funkcji:

```
def example():
    def process(sentence):
        # logika

    return process, lambda: wynik
```

---

## Status

- ✔ dziala czyszczenie tekstu ze stdin
- ✔ zachowana struktura akapitow
- ✔ `__main__` w `lab_2.py`
- 🔄 funkcje w `utils.py` do uzupelnienia
