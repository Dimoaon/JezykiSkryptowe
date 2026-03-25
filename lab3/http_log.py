import ipaddress
import sys
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlsplit

# Kolejność elementów w krotce jest stała
# i odpowiada polom używanym w zadaniach
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


def _normalize_line(line):
    # Pozwala odczytać zwykły log oraz wariant zapisany z zerowymi bajtami.
    return (
        line.replace("\ufeff", "")
        .replace("\udcff", "")
        .replace("\udcfe", "")
        .replace("\x00", "")
        .replace("\r", "")
    )


def _parse_timestamp(value):
    # UNIX timestamp interpretujemy w czasie UTC,
    # żeby wynik nie zależał od lokalnej strefy czasowej komputera.
    return datetime.fromtimestamp(float(value), timezone.utc).replace(tzinfo=None)


def _parse_optional_text(value):
    # W logu znak "-" oznacza brak wartości.
    value = value.strip()
    if value == "-":
        return None
    return value


def _parse_optional_int(value):
    # Dla pól liczbowych stosujemy tę samą zasadę co wyżej:
    # "-" zamieniamy na None, a resztę na int.
    value = value.strip()
    if value == "-":
        return None
    return int(value)


def _parse_line(line):
    fields = line.rstrip("\n").split("\t")

    if len(fields) < 15:
        raise ValueError("Linia logu ma za mało pól.")

    # Tworzymy jedną krotkę z polami potrzebnymi w laboratorium.
    # Bierzemy tylko te kolumny, których wymagają zadania.
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
        # Najpierw czyścimy linię z ewentualnych znaków technicznych.
        line = _normalize_line(line)

        if line.strip() == "":
            continue

        # Każdą poprawną linię zamieniamy na jedną krotkę.
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
        # Porównujemy kod z pola STATUS_CODE w każdej krotce.
        if entry[STATUS_CODE] == code:
            result.append(entry)

    return result


# Zadanie 4. Filtrowanie wpisów po adresie IP lub nazwie hosta.
def get_entries_by_addr(log, addr):
    if not isinstance(addr, str) or addr.strip() == "":
        raise ValueError("Adres nie może być pusty.")

    addr = addr.strip()
    addr_lower = addr.lower()
    result = []

    # Jeśli tekst wygląda jak IPv4, sprawdzamy poprawność zapisu.
    if addr.replace(".", "").isdigit():
        ipaddress.ip_address(addr)

    for entry in log:
        host = entry[HOST]

        # Adres może pasować albo do IP klienta, albo do pola host.
        if entry[ORIG_H] == addr:
            result.append(entry)
        elif host is not None and host.lower() == addr_lower:
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

        # Kody 4xx i 5xx zapisujemy osobno, bo tego wymaga treść zadania.
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
    segments = path.split("/")

    # Szukamy ostatniego segmentu, który naprawdę wygląda jak nazwa pliku.
    for segment in reversed(segments):
        if "." in segment:
            return segment.rsplit(".", 1)[1].lower()

    return None


# Zadanie 6. Filtrowanie wpisów po rozszerzeniu pliku.
def get_entries_by_extension(log, ext):
    if not isinstance(ext, str) or ext.strip() == "":
        raise ValueError("Rozszerzenie nie może być puste.")

    ext = ext.strip().lower()
    if ext.startswith("."):
        ext = ext[1:]

    result = []

    for entry in log:
        # Porównujemy rozszerzenie wyciągnięte z URI z wartością podaną przez użytkownika.
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
        # Counter zlicza, ile razy pojawia się dany adres IP klienta.
        counter[entry[ORIG_H]] += 1

    return counter.most_common(n)


# Zadanie 8. Wszystkie unikalne metody HTTP bez powtórzeń.
def get_unique_methods(log):
    methods = []

    for entry in log:
        method = entry[METHOD]

        # Zachowujemy kolejność pierwszego wystąpienia metody
        # i nie dodajemy duplikatów.
        if method is not None and method not in methods:
            methods.append(method)

    return methods


# Zadanie 9. Wpisy zadanego zakresu czasu: start <= ts < end.
def get_entries_in_time_range(log, start, end):
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise TypeError("Start i end muszą być obiektami datetime.")

    result = []

    for entry in log:
        # Zakres jest lewostronnie domknięty i prawostronnie otwarty:
        # start <= ts < end
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

        # Jeśli metoda pojawia się pierwszy raz, zaczynamy licznik od zera.
        if method not in result:
            result[method] = 0

        result[method] += 1

    return result

# Zadanie 11. Najczęściej występujące URI
def get_top_uris(log, n=10):
    if not isinstance(n, int):
        raise TypeError("Wartość musi być liczbą całkowitą.")

    if n <= 0:
        raise ValueError("Podany argument n musi być większy od zera.")

    counter = Counter()

    for entry in log:
        # Zliczamy tylko wpisy, które mają uzupełnione URI.
        if entry[URI] is not None:
            counter[entry[URI]] += 1

    return counter.most_common(n)

# Zadanie 12. Grupowanie kodów HTTP
def count_status_classes(log):
    counter = {
        "2xx": 0,
        "3xx": 0,
        "4xx": 0,
        "5xx": 0,
    }

    for entry in log:
        code = entry[STATUS_CODE]

        if code is None:
            continue

        # Dla 404 otrzymamy "4xx", dla 200 -> "2xx" itd.
        digit = code // 100
        klasa = str(digit) + "xx"

        if klasa in counter:
            counter[klasa] += 1

    return counter

# Zadanie 13. Krotka na słownik
def entry_to_dict(entry):
    # Zamieniamy krotkę na słownik, żeby później odwoływać się do pól po nazwie.
    return {
        "ts": entry[TS],
        "uid": entry[UID],
        "orig_h": entry[ORIG_H],
        "orig_p": entry[ORIG_P],
        "resp_h": entry[RESP_H],
        "resp_p": entry[RESP_P],
        "method": entry[METHOD],
        "host": entry[HOST],
        "uri": entry[URI],
        "status_code": entry[STATUS_CODE],
    }

# Zadanie 14. Log na słownik sesji
def log_to_dict(log):
    result = {}

    for entry in log:
        uid = entry[UID]
        entry_dict = entry_to_dict(entry)

        # Kluczem jest uid sesji, a wartością lista wpisów tej sesji.
        if uid not in result:
            result[uid] = []

        result[uid].append(entry_dict)

    return result

# Zadanie 15. Statystyki sesji
def print_dict_entry_dates(log_dict):
    for uid, entries in log_dict.items():
        if not entries:
            continue

        print(f"\nUID: {uid}")

        # Zbieramy wszystkie adresy IP i hosty, które pojawiły się w sesji.
        ips = set()
        hosts = set()

        for e in entries:
            ips.add(e["orig_h"])
            ips.add(e["resp_h"])
            if e["host"] is not None:
                hosts.add(e["host"])

        print("Adresy IP:", sorted(ips))
        print("Hosty:", sorted(hosts))

        total = len(entries)
        print("Liczba żądań:", total)

        # Na podstawie wszystkich znaczników czasu wyznaczamy początek i koniec sesji.
        timestamps = []
        for e in entries:
            timestamps.append(e["ts"])

        print("Pierwsze żądanie:", min(timestamps))
        print("Ostatnie żądanie:", max(timestamps))

        methods = {}
        for e in entries:
            m = e["method"]
            if m is None:
                continue
            # get(..., 0) oznacza: jeśli klucz nie istnieje, weź wartość 0.
            methods[m] = methods.get(m, 0) + 1

        print("Metody (%):")
        for m, count in methods.items():
            percent = (count / total) * 100
            print(f"  {m}: {percent:.2f}%")

        ok_count = 0

        for e in entries:
            status_code = e["status_code"]
            # Liczymy tylko poprawne odpowiedzi z klasy 2xx.
            if status_code is not None and 200 <= status_code < 300:
                ok_count += 1

        ratio = ok_count / total
        print("Stosunek kodów 2xx do wszystkich:", ratio)

# Zadanie 16. Najaktywniejsza sesja
def get_most_active_session(log_dict):
    max_uid = None
    max_count = 0

    for uid, entries in log_dict.items():
        count = len(entries)

        # Zapamiętujemy sesję z największą liczbą wpisów.
        if count > max_count:
            max_count = count
            max_uid = uid

    return max_uid

# Zadanie 17. Odtwarzanie ścieżek sesji użytkownika
def get_session_paths(log):
    result = {}

    for entry in log:
        uid = entry[UID]
        uri = entry[URI]

        if uri is None:
            continue

        # Dla każdego uid tworzymy listę odwiedzonych ścieżek.
        if uid not in result:
            result[uid] = []

        result[uid].append(uri)

    return result

# Zadanie 18. Podejrzane IP
def detect_sus(log, threshold):
    if not isinstance(threshold, int):
        raise TypeError("threshold musi być int.")

    if threshold <= 0:
        raise ValueError("threshold musi być większy od zera.")

    counter = Counter()

    for entry in log:
        ip = entry[ORIG_H]
        # Zliczamy liczbę żądań dla każdego IP.
        counter[ip] += 1

    result = []

    for ip, request_count in counter.items():
        # Za podejrzane uznajemy adresy przekraczające próg threshold.
        if request_count >= threshold:
            result.append(ip)

    return result

# Zadanie 19. Rozkład rozszerzeń plików
def get_extension_stats(log):
    counter = Counter()

    for entry in log:
        uri = entry[URI]
        ext = _get_extension_from_uri(uri)

        if ext is None:
            continue

        # Powstaje słownik typu {"html": 120, "jpg": 50, ...}.
        counter[ext] += 1

    return dict(counter)

# Zadanie 20. Mini analiza logu
def analyze_log(log):
    # Zwracamy jedną strukturę z najważniejszymi statystykami logu.
    return {
        "top_ips": get_top_ips(log, 10),
        "top_uris": get_top_uris(log, 10),
        "method_counts": count_by_method(log),
        "error_count": len(get_failed_reads(log, merge=True)),
        "status_classes": count_status_classes(log),
        "extension_stats": get_extension_stats(log),
    }


def main():
    # main() nie jest wymagany przez treść zadań,
    # ale pozwala szybko pokazać działanie wszystkich funkcji.
    log = read_log()

    if not log:
        print("Brak danych w logu.")
        return 0

    errors_4xx, errors_5xx = get_failed_reads(log)
    merged_errors = get_failed_reads(log, merge=True)

    # Przygotowujemy kilka przykładowych wartości do prezentacji działania funkcji.
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
    print()

    print("Zadanie 11 - get_top_uris(log, n=10)")
    print("Top 10 URI:", get_top_uris(log, 10))
    print()

    print("Zadanie 12 - count_status_classes(log)")
    print("Rozkład kodów HTTP:", count_status_classes(log))
    print()

    print("Zadanie 13 - entry_to_dict(entry)")
    print("Pierwszy wpis jako dict:", entry_to_dict(log[0]))
    print()

    print("Zadanie 14 - log_to_dict(log)")
    log_dict = log_to_dict(log)
    print("Liczba sesji:", len(log_dict))
    # Pokazujemy tylko jedną przykładową sesję, żeby nie wypisywać całego słownika.
    first_uid = next(iter(log_dict))
    print("Przykładowa sesja UID:", first_uid)
    print("Przykładowy wpis sesji:", log_dict[first_uid][0])
    print()

    print("Zadanie 15 - print_dict_entry_dates(log_dict)")
    print_dict_entry_dates({first_uid: log_dict[first_uid]})
    print()

    print("Zadanie 16 - get_most_active_session(log_dict)")
    uid = get_most_active_session(log_dict)
    count = len(log_dict[uid])
    print("Najaktywniejsza sesja:", uid)
    print("Liczba zapytań:", count)
    print()

    print("Zadanie 17 - get_session_paths(log)")
    session_paths = get_session_paths(log)
    print("Przykładowa sesja i jej ścieżki:", next(iter(session_paths.items())))
    print()

    print("Zadanie 18 - detect_sus(log, threshold)")
    print("Podejrzane ip:", detect_sus(log, 100))
    print()

    print("Zadanie 19 - get_extension_stats(log)")
    extension_stats = get_extension_stats(log)
    # Dla czytelności pokazujemy tylko najczęstsze rozszerzenia.
    top_extensions = sorted(
        extension_stats.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:10]
    print("Najczęstsze rozszerzenia:", top_extensions)
    print()

    print("Zadanie 20 - analyze_log(log)")
    analysis = analyze_log(log)
    # Wypisujemy najważniejsze fragmenty analizy zamiast całego słownika naraz.
    print("Najczęstsze IP:", analysis["top_ips"][:5])
    print("Najczęstsze URI:", analysis["top_uris"][:5])
    print("Rozkład metod:", analysis["method_counts"])
    print("Liczba błędów:", analysis["error_count"])
    print("Rozkład kodów HTTP:", analysis["status_classes"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
