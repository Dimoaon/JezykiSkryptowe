import os
import json
from datetime import datetime


def get_output_dir() -> str:
    # zmienna środowiskowa lub domyślnie ./converted
    return os.environ.get("CONVERTED_DIR", os.path.join(os.getcwd(), "converted"))


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

#zwraca listę wszystkich plików w katalogu i podkatalogach
def get_all_files(directory: str):
    files = []
    for root, _, filenames in os.walk(directory):
        for f in filenames:
            files.append(os.path.join(root, f))
    return files


def generate_output_name(input_path: str, target_ext: str) -> str:
    base = os.path.basename(input_path)
    name, _ = os.path.splitext(base)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{name}.{target_ext}"


def is_image(file_path: str) -> bool:
    return file_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"))


def save_history(output_dir: str, record: dict):
    history_path = os.path.join(output_dir, "history.json")

    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)

    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)