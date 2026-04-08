import sys
import os
import subprocess
from datetime import datetime
from utils import (
    get_output_dir,
    ensure_dir,
    get_all_files,
    generate_output_name,
    is_image,
    save_history
)


def convert_file(input_path: str, output_path: str, target_ext: str):
    # wybór programu
    if is_image(input_path):
        # ImageMagick
        cmd = ["magick", input_path, output_path] #budowanie komendy
        program = "magick"
    else:
        # ffmpeg // -y nadpisuje plik bez pytania //-i input
        cmd = ["ffmpeg", "-y", "-i", input_path, output_path]
        program = "ffmpeg"

    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path}: {e.stderr}")
        return None

    return program


def main():
    if len(sys.argv) < 3:
        print("Usage: python mediaconvert.py <directory> <target_format>")
        sys.exit(1)

    input_dir = sys.argv[1]
    target_format = sys.argv[2].lower()

    output_dir = get_output_dir()
    ensure_dir(output_dir) #tworzenie folderu

    files = get_all_files(input_dir)#np ["dir/a.mp4",  "dir/b.jpg", "dir/sub/c.wav" ]

    for file_path in files:
        if not os.path.isfile(file_path):
            continue #pomijam folder

        output_name = generate_output_name(file_path, target_format)
        output_path = os.path.join(output_dir, output_name)

        program_used = convert_file(file_path, output_path, target_format)

        if program_used is None:
            continue

        # zapis historii
        record = {
            "timestamp": datetime.now().isoformat(),
            "input_path": file_path,
            "output_format": target_format,
            "output_path": output_path,
            "program": program_used
        }

        save_history(output_dir, record)

        print(f"Converted: {file_path} -> {output_path}")


if __name__ == "__main__":
    main()