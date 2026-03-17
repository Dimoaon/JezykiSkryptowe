def count_sentences():
    count = 0

    def process(sentence):
        nonlocal count
        count += 1

    return process, lambda: count