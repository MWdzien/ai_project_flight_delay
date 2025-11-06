# Raport EDA — Flight Delay Prediction

## 1. Opis danych
- Liczba wierszy: 1 048 575  
- Liczba kolumn: 18  
- Źródło danych: data/01_raw/dataset_flight_delay.csv  
- Kolumny: `year`, `month`, `day_of_month`, `day_of_week`, `fl_date`, `origin`, `origin_city_name`, `origin_state_nm`, `dep_time`, `taxi_out`, `wheels_off`, `wheels_on`, `taxi_in`, `cancelled`, `air_time`, `distance`, `weather_delay`, `late_aircraft_delay`

## 2. Główne obserwacje
- Dane obejmują loty z wielu miesięcy i dni tygodnia.  
- Wartości `late_aircraft_delay` mają wyraźnie lewostronne rozkłady — większość lotów na czas, ale część z dużym opóźnieniem.  
![rozkład late_aircraft_delay][hist_late_aircraft_delay.png]
- Występują braki w danych
![macierz braków danych][missing_matrix.png]
- Większość cech numerycznych (taxi_out, taxi_in, air_time, distance) ma rozkłady skupione wokół średnich wartości, jednak z obecnymi wartościami odstającymi.
![rozkład taxi_out][hist_taxi_out.png]
![rozkład air_time][hist_air_time.png]

## 3. Problemy z jakością danych
- Braki danych w kolumnach: dep_time, cancelled oraz zmiennych zależnych od czasu (wheels_off, wheels_on).
- Duplikaty: nie wykryto (do dalszej weryfikacji).
- Nieprawidłowe typy danych:
    - fl_date jest typu object i wymaga konwersji do datetime.
    - dep_time, wheels_off, wheels_on mogą wymagać transformacji do minut/godzin w formacie czasowym.
- Outliery: znaczące w zmiennych opisujących opóźnienia i czasy kołowania.

## 4. Rekomendacje dalszych kroków
- Uzupełnienie braków danych metodami imputacji (np. medianą lub średnią).
- Konwersja godzin (dep_time, wheels_off, wheels_on) do zmiennych czasowych.
- Redukcja kolinearności poprzez usunięcie silnie skorelowanych cech (air_time lub distance).
- Normalizacja lub standaryzacja cech numerycznych.
- Utworzenie zmiennej binarnej is_delayed (np. gdy late_aircraft_delay > 15 minut).
- Sprawdzenie wpływu dni tygodnia (day_of_week) i miesięcy (month) na opóźnienia.

## 5. Załączniki
Wykresy:
- Histogramy i boxploty: docs/*.png
- Macierz korelacji: docs/correlation_heatmap.png
- Braki danych: docs/missing_matrix.png
Dane pomocnicze:
- data/intermediate/eda_outputs/