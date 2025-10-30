# 🧠 AI Project — Flight Delay Prediction

## 🎯 Cel projektu
Celem projektu jest stworzenie systemu sztucznej inteligencji służącego do **predykcji opóźnień lotów na podstawie danych historycznych o połączeniach lotniczych, liniach, pogodzie i czasie odlotów**.  
Model ma przewidywać, czy dany lot ulegnie opóźnieniu, co pozwoli pasażerom i liniom lotniczym **lepiej planować podróże i zarządzać ryzykiem opóźnień**.

Projekt realizowany jest w ramach zajęć **„Architektura systemów AI”** i obejmuje budowę kompletnego systemu AI składającego się z następujących modułów:
- **ETL / przetwarzanie danych** — implementacja pipeline’u w **Kedro** do czyszczenia, transformacji i przygotowania danych,
- **Trening modelu** — wykorzystanie AutoML lub własnego modelu klasyfikacyjnego (np. XGBoost, Random Forest),
- **API backend (.NET)** — usługa umożliwiająca wykonywanie predykcji przez HTTP endpointy,
- **UI frontend (React)** — prosty interfejs użytkownika pozwalający wprowadzić dane lotu i uzyskać przewidywany status (opóźniony / na czas),
- **Automatyzacja (Airflow)** — planowanie uruchamiania pipeline’u ETL i procesu retrainingu modelu,
- **Wdrożenie (Docker / Cloud)** — konteneryzacja projektu i uruchomienie w środowisku chmurowym.

---

## ✈️ Opis problemu
Opóźnienia lotów stanowią poważny problem dla linii lotniczych, lotnisk i pasażerów.  
Zrozumienie czynników wpływających na występowanie opóźnień może **zwiększyć efektywność operacyjną**, **zmniejszyć koszty** i **poprawić doświadczenie podróżnych**.  
Projekt ma na celu zbudowanie modelu, który na podstawie danych historycznych potrafi przewidzieć prawdopodobieństwo opóźnienia lotu.

---

## 💾 Źródło danych
Projekt korzysta z publicznego zbioru danych z serwisu Kaggle:

📊 [Flight Delay and Cancellation Data (1 Million 2024)](https://www.kaggle.com/datasets/nalisha/flight-delay-and-cancellation-data-1-million-2024?resource=download)

Dane zawierają informacje o:
- czasie odlotu i przylotu,  
- linii lotniczej,  
- trasie i długości lotu,  
- pogodzie i innych czynnikach operacyjnych,  
- wystąpieniu opóźnienia lub odwołania lotu.

Plik źródłowy:  
`data/01_raw/dataset_flight_delay.csv`

---

## 🧩 Architektura systemu
Diagram przedstawia przepływ danych i integrację komponentów systemu:

📄 [diagram (docs/architecture_diagram.png)](docs/architecture_diagram.png)

---

## 🧱 Struktura katalogów

````

ai_project_teamX/
│
├── docs/
│   └── architecture_diagram.png
│
├── src/
│   └── ai_project_teamX/   ← kod Kedro
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── models/
│
├── notebooks/
│
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md

````

## 🧑‍💻 Członkowie zespołu

| Imię i nazwisko    | Rola w projekcie | GitHub login  |
|--------------------|------------------|---------------|
|Mateusz Wdzieńkowski| Właściciel       | @MWdzien      |

---

## 🧭 Linki projektu

- 📦 Repozytorium GitHub: [link tutaj](https://github.com/MWdzien/ai_project_flight_delay)  
- 🗂️ GitHub Project Board: [link tutaj](https://github.com/users/MWdzien/projects/1)  
- 📜 Dokumentacja / diagram architektury: [link tutaj](dosc/architecture_diagram.png)  
