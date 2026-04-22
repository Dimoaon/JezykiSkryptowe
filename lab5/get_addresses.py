import csv
from pathlib import Path


def split_address(address: str):
    parts = address.strip().split()

    if not parts:
        return "", None

    last = parts[-1]

    # jeśli ostatni element zawiera cyfre to numer
    if any(c.isdigit() for c in last):
        street = " ".join(parts[:-1])
        number = last
    else:
        street = " ".join(parts)
        number = None

    return street, number


def get_addresses(path: Path, city: str):
    result = []

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f) #kazdy wiersz na słownik

        for row in reader:

            row_city = (row.get("Miejscowość") or "").strip()

            if row_city.lower() != city.lower():
                continue


            woj = (row.get("Województwo") or "").strip()

            adres = (row.get("Adres") or "").strip()

            street, number = split_address(adres)

            result.append((woj, row_city, street, number))

    return result #zwracam liste krotek z wynikami



if __name__ == "__main__":
    path = Path("data/stacje.csv")

    addresses = get_addresses(path, "Wrocław")

    print("Znalezione adresy:\n")

    for addr in addresses:
        print(addr)