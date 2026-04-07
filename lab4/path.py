import os
import sys

def get_path_dirs():
    # odczytujemy zmienną PATH, domyślnie pusty string jeśli nie istnieje
    # os.pathsep to separator katalogów – ":" na Linux/Mac, ";" na Windows
    path = os.environ.get("PATH", "")
    return path.split(os.pathsep)

def is_executable(filepath):
    # sprawdzamy dwa warunki: czy to plik (nie katalog) i czy ma bit wykonywalności
    # os.access z os.X_OK sprawdza uprawnienia do wykonania pliku
    return os.path.isfile(filepath) and os.access(filepath, os.X_OK)

def list_dirs():
    # wypisujemy każdy katalog z PATH w osobnej linii
    for directory in get_path_dirs():
        print(directory)

def list_executables():
    for directory in get_path_dirs():
        print(f"{directory}:")

        # katalog może być wpisany w PATH, ale fizycznie nie istnieć
        if not os.path.isdir(directory):
            print("  (katalog nie istnieje)")
            continue

        # os.listdir zwraca nazwy plików w katalogu
        # os.path.join łączy ścieżkę katalogu z nazwą pliku
        executables = [f for f in os.listdir(directory) if is_executable(os.path.join(directory, f))]

        if executables:
            for f in sorted(executables):
                print(f"  {f}")
        else:
            print("  (brak plików wykonywalnych)")

def print_usage():
    print("Użycie: python path.py [opcja]")
    print("  --list          wypisuje wszystkie katalogi z PATH")
    print("  --executables   wypisuje katalogi wraz z plikami wykonywalnymi")

def main():
    # wymagamy dokładnie jednej opcji
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    option = sys.argv[1]

    if option == "--list":
        list_dirs()
    elif option == "--executables":
        list_executables()
    else:
        print(f"Nieznana opcja: {option}")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
