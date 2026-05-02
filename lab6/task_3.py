import random
import string


class PasswordGenerator:
    def __init__(self, length, charset=None, count=1):
        self.length = length
        self.charset = charset if charset is not None else (string.ascii_letters + string.digits)
        self.count = count
        self.generated = 0  # ile już wygenerowano

    def __iter__(self):
        return self

    def __next__(self):
        if self.generated >= self.count:
            raise StopIteration

        password = ''.join(random.choice(self.charset) for _ in range(self.length))
        self.generated += 1
        return password

def main():
    print("Test:")
    gen = PasswordGenerator(length=5, count=3)

    try:
        print(next(gen))
        print(next(gen))
        print(next(gen))
        print(next(gen))  # tu powinien być StopIteration
    except StopIteration:
        print("StopIteration obsłużony poprawnie")

    print("\nTest pętli for")
    gen2 = PasswordGenerator(length=8, count=5)

    for password in gen2:
        print(password)


if __name__ == "__main__":
    main()