"""
Zadanie 3 – wydobywanie adresów stacji dla podanej miejscowości.

Funkcja get_addresses używa wyrażeń regularnych do wyodrębnienia
ulicy i numeru budynku z kolumny Adres w pliku stacje.csv.
"""

import csv
import re
from pathlib import Path


def get_addresses(path: Path, city: str) -> list[tuple[str, str, str, str | None]]:
    """Zwraca listę czwórek (województwo, miasto, ulica, numer) dla stacji w danym mieście.

    Numer budynku to None jeśli adres go nie zawiera.
    Wyrażenie regularne obsługuje:
      - adresy z prefiksem "ul." lub "al."  →  "ul. Chopina 35"
      - adresy bez prefiksu                 →  "Sportowa 2a"
      - adresy bez numeru                   →  "ul. Kilińskiego"
    """
    # wyrażenie regularne do rozbioru adresu na ulicę i numer:
    #
    # ^(?:ul\.|al\.)?\s*  – opcjonalny prefiks "ul." lub "al." (?: = grupa bez przechwytywania)
    #                        \. to dosłowna kropka; \s* pochłania spację po prefiksie
    # (.+?)               – nazwa ulicy, leniwe .+? zatrzymuje się przed numerem
    #                        gdyby było zachłanne .+, wzięłoby też numer do ulicy
    # (?:\s+(\d[\w/]*))?$ – opcjonalna grupa z numerem: zaczyna się od cyfry (\d),
    #                        potem litery/cyfry/slash (np. "2a", "14/16", "1/3")
    addr_re = re.compile(
        r"^(?:ul\.|al\.)?\s*"
        r"(.+?)"
        r"(?:\s+(\d[\w/]*))?$",
        re.IGNORECASE,
    )

    result: list[tuple[str, str, str, str | None]] = []

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            row_city = (row.get("Miejscowość") or "").strip()

            # porównanie bez rozróżniania wielkich liter
            if row_city.lower() != city.strip().lower():
                continue

            woj   = (row.get("Województwo") or "").strip()
            adres = (row.get("Adres") or "").strip()

            if not adres:
                # stacja bez podanego adresu
                result.append((woj, row_city, "", None))
                continue

            m = addr_re.match(adres)
            if m:
                street = m.group(1).strip()
                number = m.group(2)          # None jeśli brak numeru w adresie
            else:
                street, number = adres, None

            result.append((woj, row_city, street, number))

    return result


if __name__ == "__main__":
    import sys
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/stacje.csv")
    city = sys.argv[2] if len(sys.argv) > 2 else "Wrocław"

    addresses = get_addresses(path, city)
    print(f"Adresy stacji w miejscowości '{city}' ({len(addresses)} znaleziono):\n")
    for woj, miasto, ulica, numer in addresses:
        print(f"  ({woj}, {miasto}, {ulica!r}, {numer!r})")
