# Laboratorium 7 – Elementy programowania funkcyjnego w Pythonie

## Zadania

### Zadanie 1 – Funkcje bez pętli i instrukcji if [`task1.py`](task1.py)

Implementacje przy użyciu `map`, `filter`, `reduce` i operatora trójargumentowego:

| Funkcja | Opis | Przykład |
|---|---|---|
| `acronym(words)` | Akronim z pierwszych liter | `["Zakład", "Ubezpieczeń", "Społecznych"]` → `"ZUS"` |
| `median(lst)` | Mediana listy liczb | `[1,1,19,2,3,4,4,5,1]` → `3` |
| `pierwiastek(x, epsilon)` | Pierwiastek metodą Newtona (rekurencja) | `pierwiastek(3, 0.1)` → `1.75` |
| `make_alpha_dict(text)` | Słownik litera → słowa zawierające tę literę | `"on i ona"` → `{'o': ['on','ona'], ...}` |
| `flatten(lst)` | Spłaszczanie listy dowolnie zagnieżdżonej | `[1,[2,[3]]]` → `[1,2,3]` |
| `group_anagrams(words)` | Grupowanie anagramów po kluczu kanonicznym | `["kot","tok","pies"]` → `{'kot':['kot','tok'], ...}` |

```
python task1.py
```

---

### Zadanie 2 – Funkcje wyższego rzędu [`task2.py`](task2.py)

Predykaty działające na dowolnym iterable:

| Funkcja | Opis |
|---|---|
| `forall(pred, iterable)` | `True` jeśli **wszystkie** elementy spełniają predykat |
| `exists(pred, iterable)` | `True` jeśli **co najmniej jeden** element spełnia predykat |
| `atleast(n, pred, iterable)` | `True` jeśli **co najmniej n** elementów spełnia predykat |
| `atmost(n, pred, iterable)` | `True` jeśli **co najwyżej n** elementów spełnia predykat |

```
python task2.py
```

---

### Zadanie 3 – Iterator haseł [`task3.py`](task3.py)

Klasa `PasswordGenerator` implementująca protokół iteratora (`__iter__` / `__next__`).

```python
gen = PasswordGenerator(length=8, charset=string.ascii_letters, count=5)
for pwd in gen:
    print(pwd)
```

```
python task3.py
```

---

### Zadanie 4 – Generator przez domknięcie [`task4.py`](task4.py)

`make_generator(f)` zwraca nieskończony generator obliczający `f(1), f(2), f(3), …`

```python
squares = make_generator(lambda n: n ** 2)
list(itertools.islice(squares, 5))  # [1, 4, 9, 16, 25]

fibs = make_generator(fibonacci)
list(itertools.islice(fibs, 7))     # [1, 1, 2, 3, 5, 8, 13]
```

```
python task4.py
```

---

### Zadanie 5 – Generator z memoizacją [`task5.py`](task5.py)

`make_generator_mem(f)` działa jak `make_generator`, ale opakowuje `f` przez `functools.lru_cache`.  
Reużywa `make_generator` z zadania 4 – bez duplikowania kodu.

```
python task5.py
```

Przykładowy wynik porównania:
```
Fibonacci(30) bez memoizacji: 0.1567s
Fibonacci(30) z  memoizacją: 0.0001s
Przyspieszenie: ~1052x
```

---

### Zadanie 6 – Dekorator `@log` [`task6.py`](task6.py)

Dekorator przyjmujący poziom logowania jako argument. Loguje przez moduł `logging`.

**Dla funkcji** – czas wywołania, nazwę, argumenty, wynik, czas trwania:
```python
@log(logging.INFO)
def multiply(a, b):
    return a * b

multiply(6, 7)
# 13:57:22 [INFO] [13:57:22] multiply(6, 7) → 42  (0.00 ms)
```

**Dla klas** – loguje moment tworzenia obiektu (`__init__`):
```python
@log(logging.INFO)
class Rectangle:
    def __init__(self, width, height): ...

Rectangle(5, 3)
# 13:57:22 [INFO] Utworzono obiekt Rectangle(5, 3)  (0.00 ms)
```

```
python task6.py
```

---

## Uruchomienie wszystkich zadań

```bash
for i in 1 2 3 4 5 6; do
    echo "=== task$i.py ===" && python task$i.py
done
```
