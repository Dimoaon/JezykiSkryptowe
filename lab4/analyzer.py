import sys
import json
from collections import Counter


def analyze_file(file_path: str) -> dict:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e), "path": file_path}

    # podstawowe statystyki
    char_count = len(content)
    lines = content.splitlines()
    line_count = len(lines)

    words = content.split()
    word_count = len(words)

    # liczniki
    char_counter = Counter(content)
    word_counter = Counter(words)

    most_common_char = char_counter.most_common(1)[0][0] if char_counter else None
    most_common_word = word_counter.most_common(1)[0][0] if word_counter else None

    return {
        "path": file_path,
        "char_count": char_count,
        "word_count": word_count,
        "line_count": line_count,
        "most_common_char": most_common_char,
        "most_common_word": most_common_word,
        #zeby  print(json.dumps(result)) zadziałało
        "char_freq": dict(char_counter),
        "word_freq": dict(word_counter),
    }


def main():
    file_path = sys.stdin.read().strip()
    result = analyze_file(file_path)
    print(json.dumps(result))


if __name__ == "__main__":
    main()