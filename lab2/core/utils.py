# W tym pliku trzymamy wspolna logike dla wszystkich skryptow.
# Kazda funkcja zwraca:
# - funkcje "process", ktora wykonuje prace na pojedynczym elemencie
# - funkcje "result", ktora zwraca wynik koncowy
# Taki uklad dobrze pasuje do przetwarzania potokowego.


# Funkcje redukujace

def count_paragraphs():
    # Liczymy akapity na podstawie znakow:
    # nowy akapit zaczyna sie tam, gdzie po pustej linii
    # pojawia sie pierwszy niebialy znak.
    count = 0
    in_paragraph = False
    previous_char = ""

    def process_char(char):
        nonlocal count, in_paragraph, previous_char

        if char == "\n":
            # Podwojny enter oznacza wyjscie z aktualnego akapitu.
            if previous_char == "\n":
                in_paragraph = False
        else:
            # Pierwszy znak po pustej linii rozpoczyna nowy akapit.
            if not in_paragraph and not char.isspace():
                count += 1
                in_paragraph = True

        previous_char = char

    def result():
        return count

    return process_char, result



def count_characters():
    # Liczymy wszystkie znaki oprocz bialych znakow.
    count = 0

    def process(char):
        nonlocal count

        if not char.isspace():
            count += 1

    return process, lambda: count

def percent_sentences_with_proper_noun():
    # Liczymy procent zdan, w ktorych wystepuje nazwa wlasna.
    # W tym uproszczeniu nazwa wlasna to slowo zapisane wielka litera,
    # ale nie pierwsze slowo w zdaniu.
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

                # Pomijamy pierwsze slowo, bo ono czesto zaczyna sie wielka litera
                # tylko dlatego, ze stoi na poczatku zdania.
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



# Funkcje wyszukujace

def longest_sentence():
    # Zapamietujemy najdluzsze zdanie wedlug liczby znakow.
    longest = ""

    def process(sentence):
        nonlocal longest

        if len(sentence) > len(longest):
            longest = sentence

        return ""

    return process, lambda: longest

def longest_sentence_no_same_start_letters():
    # Szukamy najdluzszego zdania, w ktorym dwa sasiednie slowa
    # nie zaczynaja sie od tej samej litery.
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

            # Jesli dwa kolejne slowa zaczynaja sie od tej samej litery,
            # zdanie nie spelnia warunku.
            if prev_first_letter == first_letter:
                valid = False

            prev_first_letter = first_letter

        if valid and len(sentence) > len(best):
            best = sentence

        return ""

    return process, lambda: best




def first_sentence_with_multiple_clauses():
    # Za zdanie z wiecej niz jednym zdaniem podrzednym
    # przyjmujemy tu pierwsze zdanie z co najmniej dwoma przecinkami.
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


# Funkcje filtrujace

def filter_sentences_max_4_words():
    # Zwracamy tylko zdania, ktore maja najwyzej 4 wyrazy.
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
    # Zostawiamy tylko zdania zakonczone znakiem ? albo !.
    def process(sentence):
        sentence = sentence.strip()

        if sentence.endswith("?") or sentence.endswith("!"):
            return sentence

        return ""

    return process

def first_20_sentences():
    # Przepuszczamy tylko pierwsze 20 zdan.
    count = 0

    def process(sentence):
        nonlocal count

        if count < 20:
            count += 1
            return sentence

        return ""

    return process

def filter_sentences_with_conjunctions():
    # Zostawiamy tylko zdania zawierajace co najmniej dwa wyrazy
    # z listy podanej w PDF: i, oraz, ale, że, lub.
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
