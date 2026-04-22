from pathlib import Path


def group_measurement_files_by_key(path: Path):
    result = {}

    for file_path in path.iterdir():
        if not file_path.is_file():
            continue

        name = file_path.name

        # musi być .csv
        if not name.endswith(".csv"):
            continue

        # usuwam .csv
        name = name[:-4]

        parts = name.split("_") #robie liste

        # sprawdzam format
        if len(parts) < 3:
            continue

        year = parts[0]
        frequency = parts[-1]
        measurement = "_".join(parts[1:-1])

        key = (year, measurement, frequency)

        result[key] = file_path

    return result

if __name__ == "__main__":
    base = Path("data")

    grouped = group_measurement_files_by_key(base)

    print("Znalezione pliki:\n")

    for key, path in grouped.items():
        print(f"{key} -> {path}")
    #print(group_measurement_files_by_key(Path("data")))

    print("\nZnalezione pliki z kryterium 2023 i 1g:\n")
    for key, path in grouped.items():
        year, measurement, frequency = key

        if year == "2023" and frequency == "1g":
            print(key, "->", path)