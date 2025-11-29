## Cele preprocessingu

Celem etapu preprocessingu jest:
- Oczyszczenie danych z braków i wartości odstających.
- Ujednolicenie typów i formatów zmiennych (czas, kategorie, liczby).
- Stworzenie zmiennej docelowej is_delayed.
- Przeskalowanie danych numerycznych w celu poprawy jakości trenowania modeli.
- Podział zbioru na część treningową, walidacyjną i testową w sposób zrównoważony.

## Funkcje i decyzje transformacyjne
### 1. clean_data()
Funkcja odpowiedzialna za wstępne czyszczenie i standaryzację struktury danych.
| Etap                                               | Opis                                                                             | Uzasadnienie                                                      |
| -------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **Usuwanie kolumn z nadmiarem braków**             | Kolumny z >30% wartości brakujących są usuwane (`missing_col_threshold=0.3`).    | Redukcja szumu i niekompletności danych.                          |
| **Konwersja daty (`fl_date`)**                     | Zamiana na typ `datetime`.                                                       | Umożliwia dalsze operacje czasowe i grupowania.                   |
| **Konwersja kolumn kategorycznych**                | Kolumny `origin`, `origin_city_name`, `origin_state_nm` zmieniane na `category`. | Optymalizacja pamięci i kompatybilność z modelami ML.             |
| **Konwersja czasu (hhmm → minuty od północy)**     | Dla kolumn `dep_time`, `wheels_off`, `wheels_on`.                                | Ujednolicenie reprezentacji czasu jako liczby ciągłej.            |
| **Imputacja braków medianą**                       | Dla wszystkich kolumn numerycznych.                                              | Dane są prawoskośne – mediana odporna na outliery.                |
| **Usuwanie wartości odstających (IQR trimming)**   | Kolumny: `taxi_out`, `taxi_in`, `air_time`, `distance`, `late_aircraft_delay`.   | Usunięcie ekstremalnych obserwacji, które mogłyby zaburzać model. |
| **Dodanie zmiennej binarnej `is_delayed`**         | `is_delayed = 1`, jeśli `late_aircraft_delay > 15`.                              | Definicja celu klasyfikacji – lot opóźniony > 15 minut.           |
| **Zmiana typów liczbowych na niższe (`downcast`)** | Redukcja pamięci i zwiększenie wydajności.                                       |                                                                   |
| **Reset indeksu**                                  | Zapewnienie spójności po filtracjach.                                            |                                                                   |


### 2. scale_data()

Funkcja standaryzująca zmienne numeryczne.

Działanie:
- Wybiera wszystkie kolumny liczbowe (int, float) poza:
    - is_delayed (target),
    - cancelled (cecha binarna pomocnicza).
- Stosuje StandardScaler (średnia = 0, odchylenie = 1).
- Tworzy nową kopię DataFrame z przeskalowanymi kolumnami.

Uzasadnienie:
Standaryzacja zapewnia, że wszystkie cechy mają porównywalny wpływ na model.
Jest szczególnie ważna dla modeli opartych na odległościach (np. SVM, KNN, regresja logistyczna).

### 3. split_data()

Funkcja dzieli dane na trzy podzbiory: train, val, test.

Parametry:
- train_size = 0.7, val_size = 0.15, test_size = 0.15
- random_state = 42 — powtarzalność wyników.
- Jeśli istnieje kolumna is_delayed, podział jest stratyfikowany, aby zachować proporcje klas.

Uzasadnienie:
- Podział 70/15/15 zapewnia wystarczającą ilość danych treningowych przy zachowaniu niezależnej walidacji.
- Stratyfikacja chroni przed nierównym rozkładem opóźnień między zbiorami.