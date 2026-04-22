"""
Zadanie 4 – zadania a–g z użyciem wyrażeń regularnych na pliku stacje.csv.

Każde podzadanie to osobna funkcja. Uruchomienie pliku bezpośrednio
wypisuje wyniki dla domyślnej ścieżki data/stacje.csv.
"""

import csv
import re
from pathlib import Path


# ── ładowanie danych ──────────────────────────────────────────────────────────

def load_stations(path: Path) -> list[dict]:
    """Wczytuje stacje.csv i zwraca listę słowników z oczyszczonymi kluczami."""
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        result = []
        for row in reader:
            # nagłówki mogą zawierać \n – zastępujemy spacją
            clean = {
                k.replace("\n", " ").strip(): (v.strip() if v else "")
                for k, v in row.items()
            }
            result.append(clean)
    return result


# ── a) daty ───────────────────────────────────────────────────────────────────

def extract_dates(stations: list[dict]) -> list[tuple[str | None, str | None]]:
    """a) Wyodrębnia daty w formacie RRRR-MM-DD z kolumn Data uruchomienia i Data zamknięcia."""
    date_re = re.compile(r"\d{4}-\d{2}-\d{2}")
    result = []
    for s in stations:
        start = date_re.search(s.get("Data uruchomienia", ""))
        end   = date_re.search(s.get("Data zamknięcia", ""))
        # dołączamy tylko stacje mające choć jedną datę
        if start or end:
            result.append((
                start.group() if start else None,
                end.group()   if end   else None,
            ))
    return result


# ── b) współrzędne ────────────────────────────────────────────────────────────

def extract_coordinates(stations: list[dict]) -> list[tuple[float, float]]:
    """b) Wyodrębnia pary (szerokość, długość) geograficzną z 6 cyframi po kropce."""
    # \d+    – jedna lub więcej cyfr przed kropką (część całkowita)
    # \.     – dosłowna kropka (bez \ oznaczałaby "dowolny znak")
    # \d{6}  – dokładnie 6 cyfr po kropce – tyle mają współrzędne w tym pliku
    coord_re = re.compile(r"\d+\.\d{6}")
    coords = []
    for s in stations:
        lat = coord_re.search(s.get("WGS84 φ N", ""))
        lon = coord_re.search(s.get("WGS84 λ E", ""))
        if lat and lon:
            coords.append((float(lat.group()), float(lon.group())))
    return coords


# ── c) nazwy z myślnikiem ─────────────────────────────────────────────────────

def stations_with_dash(stations: list[dict]) -> list[str]:
    """c) Znajduje nazwy stacji złożone z dokładnie dwóch części oddzielonych ' - '."""
    # ^        – kotwica początku napisu
    # [^-]+    – jeden lub więcej znaków NIE będących myślnikiem (pierwsza część nazwy)
    # " - "    – dokładnie spacja-myślnik-spacja (separator między częściami)
    # [^-]+    – druga część nazwy (też bez myślnika)
    # $        – kotwica końca – zapewnia że nie ma trzeciej części
    # Dzięki [^-] zamiast .+ wzorzec nie dopasuje nazw z więcej niż jednym " - "
    two_parts_re = re.compile(r"^[^-]+ - [^-]+$")
    return [s["Nazwa stacji"] for s in stations if two_parts_re.match(s["Nazwa stacji"])]


# ── d) normalizacja nazw ──────────────────────────────────────────────────────

# tabela transliteracji polskich znaków diakrytycznych
_DIACRITICS = str.maketrans(
    "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ",
    "acelnoszzACELNOSZZ",
)

def normalize_station_names(stations: list[dict]) -> list[str]:
    """d) Zastępuje spacje podkreślnikiem i polskie znaki ich łacińskimi odpowiednikami."""
    result = []
    for s in stations:
        name = s["Nazwa stacji"]
        name = name.translate(_DIACRITICS)  # zamiana diakrytyków
        name = re.sub(r" ", "_", name)      # re.sub zastępuje wszystkie wystąpienia wzorca
        result.append(name)
    return result


# ── e) weryfikacja stacji MOB ─────────────────────────────────────────────────

def check_mob_stations(stations: list[dict]) -> list[dict]:
    """e) Zwraca stacje kończące się na 'MOB', które NIE mają rodzaju 'mobilna'.

    Zgodnie z wymaganiem: weryfikuje czy WSZYSTKIE stacje MOB mają rodzaj 'mobilna'.
    Zwraca listę stacji niespełniających tego warunku (pusta lista = wszystko OK).
    """
    mob_re = re.compile(r"MOB$")
    errors = []
    for s in stations:
        code   = s.get("Kod stacji", "")
        rodzaj = s.get("Rodzaj stacji", "").lower()
        if mob_re.search(code) and rodzaj != "mobilna":
            errors.append(s)
    return errors


# ── f) lokalizacje 3-częściowe ────────────────────────────────────────────────

def locations_three_parts(stations: list[dict]) -> list[str]:
    """f) Wyodrębnia nazwy stacji złożone z dokładnie 3 części oddzielonych ' - '."""
    three_parts_re = re.compile(r"^[^-]+ - [^-]+ - [^-]+$")
    return [s["Nazwa stacji"] for s in stations if three_parts_re.match(s["Nazwa stacji"])]


# ── g) adresy z przecinkiem i ul./al. ────────────────────────────────────────

def locations_with_street(stations: list[dict]) -> list[str]:
    """g) Znajduje adresy zawierające przecinek oraz 'ul.' lub 'al.'."""
    street_re = re.compile(r"ul\.|al\.", re.IGNORECASE)
    return [
        s["Adres"] for s in stations
        if "," in s.get("Adres", "") and street_re.search(s.get("Adres", ""))
    ]


if __name__ == "__main__":
    import sys
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/stacje.csv")
    stations = load_stations(path)

    print(f"a) Daty (pierwsze 5):")
    print(extract_dates(stations)[:5])

    print(f"\nb) Współrzędne (pierwsze 3):")
    print(extract_coordinates(stations)[:3])

    print(f"\nc) Nazwy z myślnikiem (pierwsze 5):")
    print(stations_with_dash(stations)[:5])

    print(f"\nd) Znormalizowane nazwy (pierwsze 3):")
    print(normalize_station_names(stations)[:3])

    errors = check_mob_stations(stations)
    print(f"\ne) Stacje MOB bez rodzaju 'mobilna': {len(errors)}")
    for e in errors:
        print(f"   Kod: {e['Kod stacji']}, Rodzaj: {e['Rodzaj stacji']}")

    print(f"\nf) Lokalizacje 3-częściowe (pierwsze 5):")
    print(locations_three_parts(stations)[:5])

    print(f"\ng) Adresy z przecinkiem i ul./al.:")
    print(locations_with_street(stations))
