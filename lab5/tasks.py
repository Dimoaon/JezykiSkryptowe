import csv
from pathlib import Path


def load_stations(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        result = []
        for row in reader:
            clean = {
                k.replace("\n", " ").strip(): (v.strip() if v else "")
                for k, v in row.items()
            }
            result.append(clean)

    return result



#a)
def extract_dates(stations):
    result = []

    for s in stations:
        start = s.get("Data uruchomienia", "")
        end = s.get("Data zamknięcia", "")

        # proste sprawdzenie formatu YYYY-MM-DD
        def is_date(d):
            return len(d) == 10 and d[4] == "-" and d[7] == "-"

        start = start if is_date(start) else None
        end = end if is_date(end) else None

        if start or end:
            result.append((start, end))

    return result

#b) wspolrzedne

def extract_coordinates(stations):
    coords = []

    for s in stations:
        lat = s.get("WGS84 φ N", "")
        lon = s.get("WGS84 λ E", "")

        if lat and lon:
            coords.append((float(lat), float(lon)))

    return coords



#c) nazwy z myślnikiem
def stations_with_dash(stations):
    result = []

    for s in stations:
        name = s.get("Nazwa stacji", "")
        if "-" in name:
            result.append(name)

    return result



#d) normalizacja
def normalize_station_names(stations):
    replacements =\
        {
        "ą": "a",
        "ć": "c",
        "ę": "e",
        "ł": "l",
        "ń": "n",
        "ó": "o",
        "ś": "s",
        "ż": "z",
        "ź": "z"
        }

    result = []

    for s in stations:
        name = s.get("Nazwa stacji", "")

        for pl, la in replacements.items():
            name = name.replace(pl, la)

        name = name.replace(" ", "_")

        result.append(name)

    return result



#e) MOB
def check_mob_stations(stations):
    errors = []

    for s in stations:
        code = s.get("Kod stacji", "")
        rodzaj = s.get("Rodzaj stacji", "").lower()

        if code.endswith("MOB") and rodzaj != "mobilna":
            errors.append(s)
        print("BŁĄD:")
        print("Kod:", code)
        print("Rodzaj:", rodzaj)
        print("Nazwa:", s.get("Nazwa stacji"))
        print("\n")
    return errors



#f) 3 części
def locations_three_parts(stations):
    result = []

    for s in stations:
        name = s.get("Nazwa stacji", "")

        if name.count("-") == 2:
            result.append(name)

    return result


#g) przecinek + ul./al.
def locations_with_street(stations):
    result = []

    for s in stations:
        adres = (s.get("Adres") or "").lower()

        if "," in adres and ("ul." in adres or "al." in adres):
            result.append(s.get("Adres"))

    return result

if __name__ == "__main__":
    base = Path("data")
    stations = load_stations(base / "stacje.csv")

    print("a) Daty:")
    print(extract_dates(stations)[:5])

    print("\nb) Współrzędne:")
    print(extract_coordinates(stations)[:5])

    print("\nc) Nazwy z myślnikiem:")
    print(stations_with_dash(stations)[:5])

    print("\nd) Znormalizowane nazwy:")
    print(normalize_station_names(stations)[:5])

    print("\ne) Błędy MOB:")
    print(len(check_mob_stations(stations)))

    print("\nf) 3 części:")
    print(locations_three_parts(stations)[:5])

    print("\ng) ul./al.:")
    print(locations_with_street(stations)[:5])