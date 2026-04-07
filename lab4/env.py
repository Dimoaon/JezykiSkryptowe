import os
import sys

def main():
    filters = sys.argv[1:]
    env_vars = os.environ.items()

    if filters:
        filtered = [
            (name, value)
            for name, value in env_vars
            if any(f.lower() in name.lower() for f in filters)
        ]
    else:
        filtered = list(env_vars)

    for name, value in sorted(filtered):
        print(f"{name}={value}")

if __name__ == "__main__":
    main()
