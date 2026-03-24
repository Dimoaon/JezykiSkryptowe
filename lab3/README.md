# Laboratorium 3

W katalogu `lab3` znajduje się rozwiązanie zadań `1-10` z laboratorium 3.

## Pliki

- `http_log.py` - główna implementacja funkcji z zadań 1-10,
- `data/http_first_100k.log` - plik z logami HTTP.

## Zaimplementowane funkcje

- `read_log()`
- `sort_log(log, index)`
- `get_entries_by_code(log, code)`
- `get_entries_by_addr(log, addr)`
- `get_failed_reads(log, merge=False)`
- `get_entries_by_extension(log, ext)`
- `get_top_ips(log, n=10)`
- `get_unique_methods(log)`
- `get_entries_in_time_range(log, start, end)`
- `count_by_method(log)`

## Uruchomienie

Z katalogu głównego projektu:

```bash
python3 lab3/http_log.py < lab3/data/http_first_100k.log
```

Po uruchomieniu program wypisuje przykładowe wyniki dla wszystkich funkcji
z zadań `1-10`.
