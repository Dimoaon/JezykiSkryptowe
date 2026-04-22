import csv
from pathlib import Path

def to_float(value):
    value = value.strip()
    if not value:
        return None
    return float(value.replace(",", "."))



#stacje
def parse_stations(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f) #dostaje słownik// kolumny = klucze a wartości = wartości

        result = []
        for row in reader:
            clean_row = {
                k.replace("\n", " ").strip(): v.strip() if v else v
                for k, v in row.items()
                #przechodze po wszystkich polach w tym wierszu
                #for k in row:
                    #v = row[k]
            }
            result.append(clean_row)

    return result



#pliki z pomiarami

def parse_measurement_file(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = []

        reader = csv.reader(f)

        for r in reader:
            is_not_empty = False

            for c in r:
                if c.strip() != "":
                    is_not_empty = True
                    break

            if is_not_empty:
                rows.append(r)
        #lista wszystkich niepustych wierszy

    # znajduje początek danych czyli 1 wiersz z data
    data_start = 0
    i = 0

    for row in rows:
        first = row[0]
        first = first.strip()

        if first.startswith("20") or "/" in first:
            data_start = i
            break

        i += 1

    headers = rows[:data_start]
    data_rows = rows[data_start:]

    # ile kolumn maksymalnie
    num_cols = max(len(h) for h in headers)

    result = []

    # każda kolumna
    for col in range(1, num_cols):
        station_dict = {}

        for h in headers:
            if not h:
                continue

            key = h[0].strip() #1 elem wiersza
            if key and col < len(h):
                station_dict[key] = h[col].strip()

            #{ efekt koncowy
               #"Nr": "1",
               #"Kod stacji": "A",
               #"Wskaźnik": "PM10"
            #}

        # pomijam puste kolumny
        if "Nr" not in station_dict or not station_dict["Nr"]:
            continue

        #{
            #"Nr": "3",
            #"Kod stacji": "DsWalbrzWyso"
        #} poprawna kol

        # wartosci
        for row in data_rows:
            if len(row) <= col:
                continue #pomijam jak ta kolumna nie istnieje w tym wierszu

            date = row[0].strip()
            value = row[col].strip()

            if not value:
                continue

            station_dict[date] = to_float(value)

        result.append(station_dict)

    return result


if __name__ == "__main__":
    base = Path("data")

    #stacje
    stations = parse_stations(base / "stacje.csv")
    print("Stacje:", len(stations))
    print("Pierwsza stacja:")
    print(stations[0])

    print("\n\n")

    #pomiary
    measurements = parse_measurement_file(base / "2023_As(PM10)_24g.csv")
    print("Stacje w pomiarach:", len(measurements))

    print("\nNr 1:")
    print(measurements[0])

    print("\nNr 2:")
    print(measurements[1])