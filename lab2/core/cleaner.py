def clean_text(text):
    lines = text.split("\n")

    # --- 1. УБИРАЕМ ХВОСТ (после -----) ---
    cleaned_lines = []
    for line in lines:
        if line.strip() == "-----":
            break
        cleaned_lines.append(line)

    # --- 2. УБИРАЕМ ПРЕАМБУЛУ ---
    start_index = 0
    empty_count = 0

    for i in range(min(10, len(cleaned_lines))):
        if cleaned_lines[i].strip() == "":
            empty_count += 1
            if empty_count == 2:
                start_index = i + 1
                break
        else:
            empty_count = 0

    content = cleaned_lines[start_index:]

    # --- 3. ЧИСТИМ ПРОБЕЛЫ ---
    result = []
    for line in content:
        # убираем лишние пробелы внутри строки
        cleaned = " ".join(line.strip().split())
        result.append(cleaned)

    return "\n".join(result)