from io import StringIO
import sys


def normalize_line(line):
    # Ta funkcja upraszcza pojedynczy wiersz:
    # usuwa biale znaki z poczatku i konca
    # oraz zamienia wiele spacji na jedna.
    result = ""
    pending_space = False
    i = 0

    while i < len(line):
        char = line[i]
        if char in " \t\r\n":
            # Zapamietujemy, ze pomiedzy slowami ma zostac jedna spacja.
            if result:
                pending_space = True
        else:
            if pending_space:
                result += " "
                pending_space = False
            result += char
        i += 1

    return result


def iter_clean_chunks(input_stream):
    # Czytamy plik linia po linii, zeby dzialac potokowo
    # i nie trzymac calego tekstu naraz w pamieci.
    buffer = ""
    checked_lines = 0
    empty_count = 0
    content_started = False

    for raw_line in input_stream:
        cleaned_line = normalize_line(raw_line)

        # Linia z piecioma myslnikami oznacza poczatek informacji o wydaniu.
        # Wszystko dalej ignorujemy.
        if cleaned_line == "-----":
            break

        if not content_started:
            checked_lines += 1
            buffer += cleaned_line + "\n"

            # Dwie puste linie w pierwszych 10 wierszach oznaczaja koniec preambuly.
            if cleaned_line == "":
                empty_count += 1
                if empty_count == 2:
                    buffer = ""
                    content_started = True
            else:
                empty_count = 0

            if checked_lines == 10 and not content_started:
                # Jesli w pierwszych 10 liniach nie ma dwoch pustych wierszy,
                # uznajemy, ze preambuly nie bylo i wypisujemy bufor jako tresc.
                yield buffer
                buffer = ""
                content_started = True
            continue

        # Gdy tresc sie juz zaczela, zwracamy kolejne oczyszczone linie.
        yield cleaned_line + "\n"

    if not content_started and buffer:
        yield buffer


def iter_clean_characters(input_stream):
    # Zamieniamy oczyszczone linie na strumien pojedynczych znakow.
    # To przydaje sie parserowi i funkcjom liczacym znaki lub akapity.
    for chunk in iter_clean_chunks(input_stream):
        i = 0
        while i < len(chunk):
            yield chunk[i]
            i += 1


def clean_stream(input_stream, output_stream):
    # Najprostsza wersja czyszczenia:
    # bierzemy dane ze stdin i zapisujemy oczyszczony wynik na stdout.
    for chunk in iter_clean_chunks(input_stream):
        output_stream.write(chunk)


def clean_text(text):
    # Wersja pomocnicza do testow:
    # przyjmuje zwykla zmienna tekstowa zamiast strumienia.
    input_stream = StringIO(text)
    output_stream = StringIO()
    clean_stream(input_stream, output_stream)
    return output_stream.getvalue()


if __name__ == "__main__":
    # Pozwala uruchomic sam cleaner jako osobny skrypt.
    clean_stream(sys.stdin, sys.stdout)
