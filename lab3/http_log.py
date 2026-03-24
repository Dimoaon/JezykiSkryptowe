import ipaddress
import sys
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlsplit

# Kolejność elementów w krotce jest stała
# i odpowiada polom używanym w zadaniach 1-10.
ENTRY_LENGTH = 10
TS = 0
UID = 1
ORIG_H = 2
ORIG_P = 3
RESP_H = 4
RESP_P = 5
METHOD = 6
HOST = 7
URI = 8
STATUS_CODE = 9


def _parse_timestamp(value):
    # UNIX timestamp interpretujemy w czasie UTC,
    # żeby wynik nie zależał od lokalnej strefy czasowej komputera.
    return datetime.fromtimestamp(float(value), timezone.utc).replace(tzinfo=None)


def _parse_optional_text(value):
    value = value.strip()
    if value == "-":
        return None
    return value


def _parse_optional_int(value):
    value = value.strip()
    if value == "-":
        return None
    return int(value)


def _parse_line(line):
    fields = line.rstrip("\n").split("\t")

    # Tworzymy krotkę zawierającą co najmniej pola opisane w zadaniu 0.
    return (
        _parse_timestamp(fields[0]),
        fields[1],
        fields[2],
        int(fields[3]),
        fields[4],
        int(fields[5]),
        _parse_optional_text(fields[7]),
        _parse_optional_text(fields[8]),
        _parse_optional_text(fields[9]),
        _parse_optional_int(fields[14]),
    )


# Zadanie 1. Wczytywanie logów z wejścia standardowego do krotek.
def read_log():
    log = []

    for line in sys.stdin:
        if line.strip() == "":
            continue
        log.append(_parse_line(line))

    return log


# Zadanie 2. Sortowanie logów według wskazanego indeksu krotki.
def sort_log(log, index):
    if not isinstance(index, int):
        raise TypeError("Index musi być liczbą całkowitą.")

    if index < 0 or index >= ENTRY_LENGTH:
        raise IndexError("Niepoprawny indeks krotki.")

    # None trafia na koniec, żeby sortowanie działało także dla pustych pól.
    return sorted(log, key=lambda entry: (entry[index] is None, entry[index]))


# Zadanie 3. Filtrowanie wpisów po kodzie HTTP.
def get_entries_by_code(log, code):
    if not isinstance(code, int):
        raise TypeError("Kod HTTP musi być liczbą całkowitą.")

    if code < 100 or code > 599:
        raise ValueError("Kod HTTP musi być w zakresie 100-599.")

    result = []

    for entry in log:
        if entry[STATUS_CODE] == code:
            result.append(entry)

    return result


# Zadanie 4. Filtrowanie wpisów po adresie IP lub nazwie hosta.
def get_entries_by_addr(log, addr):
    if not isinstance(addr, str) or addr.strip() == "":
        raise ValueError("Adres nie może być pusty.")

    addr = addr.strip()
    result = []

    # Jeśli tekst wygląda jak IPv4, sprawdzamy poprawność zapisu.
    if addr.replace(".", "").isdigit():
        ipaddress.ip_address(addr)

    for entry in log:
        if entry[ORIG_H] == addr or entry[HOST] == addr:
            result.append(entry)

    return result


# Zadanie 5. Zwracanie wpisów z błędami 4xx i 5xx.
def get_failed_reads(log, merge=False):
    errors_4xx = []
    errors_5xx = []

    for entry in log:
        status_code = entry[STATUS_CODE]

        if status_code is None:
            continue

        if 400 <= status_code < 500:
            errors_4xx.append(entry)
        elif 500 <= status_code < 600:
            errors_5xx.append(entry)

    if merge:
        return errors_4xx + errors_5xx

    return errors_4xx, errors_5xx


def _get_extension_from_uri(uri):
    if uri is None:
        return None

    # Pomijamy parametry w URI, np. /image.jpg?width=1024.
    path = urlsplit(uri).path

    if "." not in path:
        return None

    return path.rsplit(".", 1)[1].lower()


# Zadanie 6. Filtrowanie wpisów po rozszerzeniu pliku.
def get_entries_by_extension(log, ext):
    if not isinstance(ext, str) or ext.strip() == "":
        raise ValueError("Rozszerzenie nie może być puste.")

    ext = ext.strip().lower()
    if ext.startswith("."):
        ext = ext[1:]

    result = []

    for entry in log:
        if _get_extension_from_uri(entry[URI]) == ext:
            result.append(entry)

    return result


# Zadanie 7. Najczęściej występujące adresy IP.
def get_top_ips(log, n=10):
    if not isinstance(n, int):
        raise TypeError("n musi być liczbą całkowitą.")

    if n <= 0:
        raise ValueError("n musi być większe od zera.")

    counter = Counter()

    for entry in log:
        counter[entry[ORIG_H]] += 1

    return counter.most_common(n)


# Zadanie 8. Wszystkie unikalne metody HTTP bez powtórzeń.
def get_unique_methods(log):
    methods = []

    for entry in log:
        method = entry[METHOD]

        if method is not None and method not in methods:
            methods.append(method)

    return methods


# Zadanie 9. Wpisy zadanego zakresu czasu: start <= ts < end.
def get_entries_in_time_range(log, start, end):
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise TypeError("Start i end muszą być obiektami datetime.")

    result = []

    for entry in log:
        if start <= entry[TS] < end:
            result.append(entry)

    return result


# Zadanie 10. Liczba zapytań dla każdej metody HTTP.
def count_by_method(log):
    result = {}

    for entry in log:
        method = entry[METHOD]

        if method is None:
            continue

        if method not in result:
            result[method] = 0

        result[method] += 1

    return result


def main():
    log = read_log()

    if not log:
        print("Brak danych w logu.")
        return 0

    errors_4xx, errors_5xx = get_failed_reads(log)
    merged_errors = get_failed_reads(log, merge=True)

    example_code = 200
    if len(get_entries_by_code(log, example_code)) == 0:
        example_code = 404

    example_addr = log[0][ORIG_H]
    example_start = log[0][TS]
    example_end = log[min(100, len(log) - 1)][TS]

    print("Zadanie 1 - read_log()")
    print("Liczba wpisów:", len(log))
    print("Pierwszy wpis:", log[0])
    print()

    print("Zadanie 2 - sort_log(log, index)")
    print("Pierwsze 3 wpisy po sortowaniu po kodzie statusu:")
    for entry in sort_log(log, STATUS_CODE)[:3]:
        print(entry)
    print()

    print("Zadanie 3 - get_entries_by_code(log, code)")
    print(f"Liczba wpisów z kodem {example_code}:", len(get_entries_by_code(log, example_code)))
    print()

    print("Zadanie 4 - get_entries_by_addr(log, addr)")
    print(f"Liczba wpisów dla adresu {example_addr}:", len(get_entries_by_addr(log, example_addr)))
    print()

    print("Zadanie 5 - get_failed_reads(log, merge=False)")
    print("Liczba błędów 4xx:", len(errors_4xx))
    print("Liczba błędów 5xx:", len(errors_5xx))
    print("Liczba wszystkich błędów po merge=True:", len(merged_errors))
    print()

    print("Zadanie 6 - get_entries_by_extension(log, ext)")
    print("Liczba wpisów dla rozszerzenia 'html':", len(get_entries_by_extension(log, "html")))
    print()

    print("Zadanie 7 - get_top_ips(log, n=10)")
    print("Top 10 adresów IP:", get_top_ips(log, 10))
    print()

    print("Zadanie 8 - get_unique_methods(log)")
    print("Unikalne metody HTTP:", get_unique_methods(log))
    print()

    print("Zadanie 9 - get_entries_in_time_range(log, start, end)")
    print(
        "Liczba wpisów w przykładowym zakresie czasu:",
        len(get_entries_in_time_range(log, example_start, example_end)),
    )
    print()

    print("Zadanie 10 - count_by_method(log)")
    print("Liczba zapytań per metoda:", count_by_method(log))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
