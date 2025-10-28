# AI Project – Flight Delay Prediction

## Cel projektu
Celem projektu jest stworzenie kompletnego pipeline’u AI do predykcji opóźnień lotów na podstawie danych historycznych.

## Architektura
System składa się z następujących modułów:
- ETL i eksploracja danych – Kedro
- Trening modelu – Scikit-learn / PyCaret
- API predykcyjne – .NET
- Frontend – React
- Automatyzacja pipeline’u – Apache Airflow
- Wdrożenie – Docker

## Dane
Źródło: [Flight Delay and Cancellation Data (Kaggle)](https://www.kaggle.com/datasets/nalisha/flight-delay-and-cancellation-data-1-million-2024)

## Uruchomienie
```bash
kedro new
kedro run
