# Laboratorium 3

W katalogu `lab3` znajduje się rozwiązanie zadań `1-20` z laboratorium 3.

## Pliki

- `http_log.py` - główna implementacja funkcji z zadań 1-20,
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
- `get_top_uris(log, n=10)`
- `count_status_classes(log`
- `entry_to_dict(entry)`
- `print_dict_entry_dates(log_dict)`
- `get_most_active_session(log_dict)`
- `get_session_paths(log)`
- `detect_sus(log, threshold)`
- `get_extension_stats(log)`
- `analyze_log(log)`

## Uruchomienie

Z katalogu głównego projektu:

```bash
python3 lab3/http_log.py < lab3/data/text.log
```

Po uruchomieniu program wypisuje przykładowe wyniki dla wszystkich funkcji
z zadań `1-20`.
