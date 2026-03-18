#Funkcje redukujace

def count_words():
    count = 0

    def process(sentence):
        nonlocal count
        in_word = False

        for c in sentence:
            if c.isalpha():
                if not in_word:
                    count += 1
                    in_word = True
            else:
                in_word = False

        return ""

    return process, lambda: count

def count_paragraphs():
    count = 0
    in_paragraph = False
    previous_char = ""

    def process_char(char):
        nonlocal count, in_paragraph, previous_char

        if char == "\n":
            if previous_char == "\n":
                in_paragraph = False
        else:
            if not in_paragraph and not char.isspace():
                count += 1
                in_paragraph = True

        previous_char = char

    def result():
        return count

    return process_char, result



def count_characters():
    count = 0

    def process(sentence):
        nonlocal count

        for c in sentence:
            if not c.isspace():
                count += 1

        return ""

    return process, lambda: count

def percent_sentences_with_proper_noun():
    total_sentences = 0
    sentences_with_proper = 0

    def process(sentence):
        nonlocal total_sentences, sentences_with_proper

        total_sentences += 1

        i = 0
        word_index = 0
        has_proper = False

        while i < len(sentence):
            # pomijam znaki niebedace literami
            while i < len(sentence) and not sentence[i].isalpha():
                i += 1

            start = i

            while i < len(sentence) and sentence[i].isalpha():
                i += 1

            if start < i:
                word = sentence[start:i]

                if word_index > 0 and word[0].isupper():
                    has_proper = True

                word_index += 1

        if has_proper:
            sentences_with_proper += 1

        return ""

    def result():
        if total_sentences == 0:
            return 0
        return (sentences_with_proper / total_sentences) * 100

    return process, result



#Wyszukujace

def longest_sentence():
    longest = ""

    def process(sentence):
        nonlocal longest

        if len(sentence) > len(longest):
            longest = sentence

        return ""

    return process, lambda: longest

def longest_sentence_no_same_start_letters():
    best = ""

    def process(sentence):
        nonlocal best

        i = 0
        prev_first_letter = ""
        valid = True

        while i < len(sentence):
            # pomijam nie litery
            while i < len(sentence) and not sentence[i].isalpha():
                i += 1

            if i >= len(sentence):
                break

            # pierwsza litera slowa
            first_letter = sentence[i].lower()

            # przechodze cale slowo
            while i < len(sentence) and sentence[i].isalpha():
                i += 1

            # sprawdzam warunkek
            if prev_first_letter == first_letter:
                valid = False

            prev_first_letter = first_letter

        if valid and len(sentence) > len(best):
            best = sentence

        return ""

    return process, lambda: best




def first_sentence_with_multiple_clauses():
    found = ""

    def process(sentence):
        nonlocal found

        if found:
            return ""

        comma_count = 0

        for c in sentence:
            if c == ",":
                comma_count += 1

        if comma_count >= 2:
            found = sentence

        return ""

    return process, lambda: found


#filtrujace

def filter_sentences_max_4_words():
    def process(sentence):
        word_count = 0
        in_word = False

        for c in sentence:
            if c.isalpha():
                if not in_word:
                    word_count += 1
                    in_word = True
            else:
                in_word = False

        if word_count <= 4:
            return sentence

        return ""

    return process

def filter_questions_and_exclamations():
    def process(sentence):
        sentence = sentence.strip()

        if sentence.endswith("?") or sentence.endswith("!"):
            return sentence

        return ""

    return process

def first_20_sentences():
    count = 0

    def process(sentence):
        nonlocal count

        if count < 20:
            count += 1
            return sentence

        return ""

    return process

def filter_sentences_with_conjunctions():
    def process(sentence):
        i = 0
        count = 0

        while i < len(sentence):
            # pomijam znaki ktore nie sa literami
            while i < len(sentence) and not sentence[i].isalpha():
                i += 1

            start = i

            while i < len(sentence) and sentence[i].isalpha():
                i += 1

            if start < i:
                word = sentence[start:i].lower()

                if word == "i" or word == "oraz" or word == "ale" or word == "że" or word == "lub":
                    count += 1

        if count >= 2:
            return sentence

        return ""

    return process

