"""
Zadanie rozszerzające 2 – wykrywanie anomalii w danych pomiarowych.

Funkcja detect_anomalies przyjmuje płaską listę pomiarów i sprawdza trzy reguły:
  1. bad_data – zbyt duży udział wartości None / zerowych / ujemnych (uszkodzony czujnik)
  2. jump     – nagły skok wartości między kolejnymi pomiarami (błąd pomiaru)
  3. spike    – przekroczenie progów alarmowych dla danej wielkości (np. PM10 > 500)
"""

from datetime import datetime

# progi alarmowe wg standardów WHO / dyrektywy EU dla typowych wielkości (µg/m³)
SPIKE_THRESHOLDS: dict[str, float] = {
    "PM10":  500.0,
    "PM2.5": 300.0,
    "PM25":  300.0,   # alternatywna nazwa bez kropki
    "NO2":   400.0,
    "SO2":   500.0,
    "CO":  30000.0,   # CO mierzone w µg/m³ – wartości rzędu tysięcy są normalne
    "O3":    400.0,
}

# wartości domyślne eksportowane do task5.py i task_ext1.py
DEFAULT_SPIKE     = 1000.0   # próg dla nieznanych wielkości
DEFAULT_DELTA     = 200.0    # max skok między kolejnymi pomiarami
DEFAULT_BAD_RATIO = 0.3      # max 30% złych wartości w serii


def detect_anomalies(
    measurements: list[tuple[datetime, float | None, str, str]],
    delta_threshold: float = DEFAULT_DELTA,
    bad_ratio_threshold: float = DEFAULT_BAD_RATIO,
    spike_threshold: float | None = None,
) -> list[dict]:
    """Wykrywa anomalie w danych pomiarowych.

    Argumenty:
        measurements      – lista krotek (czas, wartość|None, kod_stacji, wielkość)
        delta_threshold   – maksymalny dozwolony skok między kolejnymi ważnymi pomiarami
        bad_ratio_threshold – maksymalny dopuszczalny udział złych wartości (None/0/ujemne)
        spike_threshold   – nadpisuje domyślny próg alarmowy dla danej wielkości

    Zwraca listę słowników z kluczami: type, station, quantity, detail.
    """
    from collections import defaultdict

    # grupujemy pomiary według pary (stacja, wielkość) – każda para analizowana osobno
    groups: dict[tuple[str, str], list[tuple[datetime, float | None]]] = defaultdict(list)
    for dt, val, station, quantity in measurements:
        groups[(station, quantity)].append((dt, val))

    results: list[dict] = []

    for (station, quantity), records in groups.items():
        # sort jest konieczny dla reguły jump – musimy porównywać KOLEJNE pomiary
        # bez sortowania moglibyśmy porównać pomiar z marca z pomiarem ze stycznia
        records.sort(key=lambda r: r[0])

        all_values = [v for _, v in records]
        total = len(all_values)
        if total == 0:
            continue

        # próg spike: jawnie podany → z tablicy progów → wartość domyślna
        limit = spike_threshold or SPIKE_THRESHOLDS.get(quantity.upper(), DEFAULT_SPIKE)

        # ── reguła 1: złe dane ──────────────────────────────────────────────
        # None oznacza brak pomiaru, 0 i ujemne – prawdopodobnie awarię czujnika
        bad = sum(1 for v in all_values if v is None or v <= 0)
        if bad / total > bad_ratio_threshold:
            results.append({
                "type":     "bad_data",
                "station":  station,
                "quantity": quantity,
                "detail":   (
                    f"{bad}/{total} wartości to None/zero/ujemne "
                    f"({bad / total:.0%})"
                ),
            })

        # filtrujemy None przed analizą skoków i spike'ów
        valid = [(dt, v) for dt, v in records if v is not None]

        # ── reguła 2: nagły skok ─────────────────────────────────────────────
        # zip(valid, valid[1:]) to klasyczny Python trick na pary sąsiednich elementów:
        # valid      = [(t1,v1), (t2,v2), (t3,v3), ...]
        # valid[1:]  = [(t2,v2), (t3,v3), ...]
        # zip daje:  = [(t1,v1,t2,v2), (t2,v2,t3,v3), ...]  czyli kolejne pary
        for (dt1, v1), (dt2, v2) in zip(valid, valid[1:]):
            delta = abs(v2 - v1)
            if delta > delta_threshold:
                results.append({
                    "type":     "jump",
                    "station":  station,
                    "quantity": quantity,
                    "detail":   (
                        f"Δ={delta:.2f} między {dt1} a {dt2} "
                        f"({v1:.2f} → {v2:.2f})"
                    ),
                })

        # ── reguła 3: przekroczenie progu alarmowego ─────────────────────────
        for dt, v in valid:
            if v > limit:
                results.append({
                    "type":     "spike",
                    "station":  station,
                    "quantity": quantity,
                    "detail":   f"{v:.2f} > {limit} o {dt}",
                })

    return results
