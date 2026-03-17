def iter_characters(source):
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
    sentence = ""
    previous_char = ""

    for char in iter_characters(source):
        sentence += char

        # koniec zdania po znaku interpunkcyjnym
        if char in ".!?":
            # sprawdzenie: czy to nie jest jedyna litera (np. "I.")
            if len(sentence.strip()) <= 3:
                previous_char = char
                continue

            process_function(sentence.strip())
            sentence = ""

        # koniec akapitu = koniec zdania
        elif char == "\n":
            # jezeli wystepuje podwojny znak nowej linii
            if previous_char == "\n":
                if sentence.strip():
                    process_function(sentence.strip())
                    sentence = ""

        previous_char = char

    # pozostala czesc
    if sentence.strip():
        process_function(sentence.strip())
