def process_sentences(text, process_function):
    sentence = ""

    i = 0
    while i < len(text):
        c = text[i]
        sentence += c

        # koniec zdania po znaku interpunkcyjnym
        if c in ".!?":
            # sprawdzenie: czy to nie jest jedyna litera (np. "I.")
            if len(sentence.strip()) <= 3:
                i += 1
                continue

            process_function(sentence.strip())
            sentence = ""

        # koniec akapitu = koniec zdania
        elif c == "\n":
            # jezeli wystepuje podwojny znak nowej linii
            if i + 1 < len(text) and text[i + 1] == "\n":
                if sentence.strip():
                    process_function(sentence.strip())
                    sentence = ""

        i += 1

    # pozostala czesc
    if sentence.strip():
        process_function(sentence.strip())
