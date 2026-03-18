def iter_characters(source):
    # Parser moze dostac albo strumien (np. stdin),
    # albo juz gotowy tekst / generator znakow.
    if hasattr(source, "read"):
        while True:
            char = source.read(1)
            if not char:
                break
            yield char
        return

    for char in source:
        yield char


def process_sentences(source, process_function):
    # Zbieramy kolejne znaki do momentu,
    # az trafimy na koniec zdania albo koniec akapitu.
    sentence = ""
    previous_char = ""

    for char in iter_characters(source):
        sentence += char

        # Kropka, wykrzyknik i pytajnik traktujemy jako koniec zdania.
        if char in ".!?":
            process_function(sentence.strip())
            sentence = ""

        # Podwojny enter oznacza koniec akapitu,
        # a wedlug PDF pusty wiersz wymusza tez koniec zdania.
        elif char == "\n":
            if previous_char == "\n":
                if sentence.strip():
                    process_function(sentence.strip())
                    sentence = ""

        previous_char = char

    # Jesli po petli zostalo jeszcze niedomkniete zdanie,
    # tez je przekazujemy dalej.
    if sentence.strip():
        process_function(sentence.strip())


def write_first_sentences(source, output_stream, limit):
    # Ta funkcja sluzy do pipeline'u:
    # wypisuje tylko pierwsze "limit" zdan,
    # ale zachowuje oryginalne znaki nowej linii.
    sentence = ""
    previous_char = ""
    count = 0

    for char in iter_characters(source):
        output_stream.write(char)
        sentence += char

        if char in ".!?":
            count += 1
            sentence = ""
            if count == limit:
                break

        elif char == "\n":
            if previous_char == "\n":
                if sentence.strip():
                    count += 1
                    sentence = ""
                    if count == limit:
                        break

        previous_char = char
