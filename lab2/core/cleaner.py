from io import StringIO


def normalize_line(line):
    result = ""
    pending_space = False
    i = 0

    while i < len(line):
        char = line[i]
        if char in " \t\r\n":
            if result:
                pending_space = True
        else:
            if pending_space:
                result += " "
                pending_space = False
            result += char
        i += 1

    return result


def clean_stream(input_stream, output_stream):
    buffer = ""
    checked_lines = 0
    empty_count = 0
    content_started = False

    for raw_line in input_stream:
        cleaned_line = normalize_line(raw_line)

        if cleaned_line == "-----":
            break

        if not content_started:
            checked_lines += 1
            buffer += cleaned_line + "\n"

            if cleaned_line == "":
                empty_count += 1
                if empty_count == 2:
                    buffer = ""
                    content_started = True
            else:
                empty_count = 0

            if checked_lines == 10 and not content_started:
                output_stream.write(buffer)
                buffer = ""
                content_started = True
            continue

        output_stream.write(cleaned_line + "\n")

    if not content_started:
        output_stream.write(buffer)


def clean_text(text):
    input_stream = StringIO(text)
    output_stream = StringIO()
    clean_stream(input_stream, output_stream)
    return output_stream.getvalue()
