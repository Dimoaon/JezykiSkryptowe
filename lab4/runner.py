import sys
import os
import json
import subprocess
from collections import Counter


def run_analyzer(file_path: str) -> dict:
    try:
        process = subprocess.run(
            ["python", "analyzer.py"],
            input=file_path,
            text=True,
            capture_output=True
        )

        return json.loads(process.stdout)

    except Exception as e:
        return {"error": str(e), "path": file_path}


def main():
    if len(sys.argv) < 2:
        print("Usage: python runner.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]

    results = []

    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)

            #tylko pliki tekstowe
            if not file.endswith(".txt"):
                continue

            result = run_analyzer(path)

            if "error" not in result:
                results.append(result)

    # zapis listy słowników
    print("LISTA WYNIKOW")
    print(json.dumps(results, indent=4))

    total_files = len(results)
    total_chars = sum(r["char_count"] for r in results)
    total_words = sum(r["word_count"] for r in results)
    total_lines = sum(r["line_count"] for r in results)

    char_counter = Counter()
    word_counter = Counter()

    for r in results:
        char_counter.update(r.get("char_freq", {}))
        word_counter.update(r.get("word_freq", {}))

    most_common_char = char_counter.most_common(1)[0][0] if char_counter else None
    most_common_word = word_counter.most_common(1)[0][0] if word_counter else None

    summary = {
        "files_processed": total_files,
        "total_chars": total_chars,
        "total_words": total_words,
        "total_lines": total_lines,
        "most_common_char": most_common_char,
        "most_common_word": most_common_word,
    }

    print("\nPODSUMOWANIE")
    print(json.dumps(summary, indent=4))


if __name__ == "__main__":
    main()