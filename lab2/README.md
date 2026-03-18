# Lab 2 - Podstawy Pythona. Praca z funkcjami

## Opis
Program bazowy:
- czyta dane ze standardowego wejscia,
- usuwa preambule,
- ignoruje wszystko po linii `-----`,
- zachowuje strukture akapitow,
- usuwa zbedne biale znaki na poczatku i koncu linii
  oraz nadmiarowe spacje wewnatrz linii.

Dodatkowe funkcjonalnosci z punktu 3 PDF zostaly rozdzielone na osobne
moduly uruchamiane z terminala przez `stdin` i `stdout`.

Plik `core/utils.py` zawiera wspolna logike dla tych modulow i nie jest
uruchamiany bezposrednio z terminala.

## Struktura

```text
lab2/
├── core/
│   ├── cleaner.py
│   ├── parser.py
│   └── utils.py
├── data/
├── lab_2.py
├── count_paragraphs.py
├── count_characters.py
├── percent_sentences_with_proper_noun.py
├── longest_sentence.py
├── longest_sentence_no_same_start_letters.py
├── first_sentence_with_multiple_clauses.py
├── filter_sentences_max_4_words.py
├── filter_questions_and_exclamations.py
├── first_20_sentences.py
├── filter_sentences_with_conjunctions.py
├── JS_Lab_02.pdf
└── README.md
```

## Uruchomienie

Z katalogu `lab2`:

```bash
python lab_2.py < data/dziewczynka_z_zapalkami.txt
python count_paragraphs.py < data/dziewczynka_z_zapalkami.txt
python count_characters.py < data/dziewczynka_z_zapalkami.txt
python percent_sentences_with_proper_noun.py < data/dziewczynka_z_zapalkami.txt
python longest_sentence.py < data/dziewczynka_z_zapalkami.txt
python longest_sentence_no_same_start_letters.py < data/dziewczynka_z_zapalkami.txt
python first_sentence_with_multiple_clauses.py < data/dziewczynka_z_zapalkami.txt
python filter_sentences_max_4_words.py < data/dziewczynka_z_zapalkami.txt
python filter_questions_and_exclamations.py < data/dziewczynka_z_zapalkami.txt
python first_20_sentences.py < data/dziewczynka_z_zapalkami.txt
python filter_sentences_with_conjunctions.py < data/dziewczynka_z_zapalkami.txt
```

## Pipeline

Przyklad potokowego przetwarzania danych:

```bash
cat data/dziewczynka_z_zapalkami.txt | python first_20_sentences.py | python count_paragraphs.py
```

Dla aktualnych danych wynik powinien wynosic:

```text
5
```

## Podzial odpowiedzialnosci

- `core/cleaner.py` - czyszczenie danych wejsciowych
- `core/parser.py` - przetwarzanie tekstu znak po znaku i dzielenie na zdania
- `core/utils.py` - wspolne funkcje redukujace, wyszukujace i filtrujace
- pliki w katalogu glownym `lab2/` - osobne moduly uruchamiane z terminala

## Po co jest `utils.py`

Plik `core/utils.py` jest potrzebny, bo:
- przechowuje wspolna logike dla wielu skryptow,
- pozwala nie powielac tego samego kodu w kazdym pliku,
- odpowiada zasadzie z PDF, ze wspolne funkcje powinny byc umieszczone
  w osobnym module, aby mozna bylo je ponownie uzywac.

## Zgodnosc z PDF

Projekt jest przygotowany zgodnie z glownymi zalozeniami dokumentu:
- `lab_2.py` realizuje tylko punkt 2 PDF
- kazda funkcjonalnosc z punktu 3 ma osobny plik
- skrypty korzystaja z `stdin` i `stdout`
- dziala konstrukcja `if __name__ == "__main__":`
- dziala potok:
  `first_20_sentences.py | count_paragraphs.py`
