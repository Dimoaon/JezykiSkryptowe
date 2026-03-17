# Lab 2 – Text Processing

## Opis
Program czyta tekst ze stdin, czyści go i dzieli na zdania.  
Następnie można wykonywać różne operacje na zdaniach (np. liczenie).

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
```

---

## Jak działa

- `cleaner.py` – usuwa nagłówki i zbędny tekst  
- `parser.py` – dzieli tekst na zdania  
- `utils.py` – funkcje do przetwarzania zdań  

Parser wywołuje funkcję dla każdego zdania:

```
process_sentences(text, process_function)
```

---

## Podział pracy

### Moja część
- cleaner  
- parser  
- struktura projektu  
- pipeline (stdin → output)

### Partner
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

- ✔ działa  
- ✔ parser i cleaner gotowe  
- 🔄 utils do uzupełnienia  