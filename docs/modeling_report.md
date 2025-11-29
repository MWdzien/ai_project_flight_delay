# Raport z ewaluacji modeli – Flight Delay Prediction

## 1. Cel

Celem tego etapu było porównanie wyników dwóch podejść do modelowania opóźnień lotów:

1. **Baseline** – prosty model klasyfikacyjny (np. Decision Tree, Logistic Regression).  
2. **AutoML** – automatyczny wybór najlepszych modeli klasyfikacyjnych i ich hiperparametrów.

---

## 2. Metryki ewaluacyjne

W przypadku klasyfikacji zastosowano następujące miary:

- **Accuracy** – ogólna dokładność modelu.  
- **Precision** – dokładność dla klasy opóźnionych lotów.  
- **Recall** – odsetek prawidłowo wykrytych opóźnionych lotów.  
- **F1-score** – średnia harmoniczna Precision i Recall.  
- **ROC AUC** – pole pod krzywą ROC (jakość predykcji probabilistycznych).  

Dla regresji (jeśli dotyczy) stosuje się:

- **RMSE**, **MAE**, **R²**.

---

## 3. Wyniki – klasyfikacja

| Model       | Accuracy | Precision | Recall  | F1-score | ROC AUC |
|------------ |---------|-----------|--------|----------|---------|
| Baseline    | 0.5651  | 0.5000    | 0.0000 | 0.0000   | 0.5000  |
| AutoML (RF) | 0.8630  | 0.7868    | 0.9397 | 0.8565   | 0.9193  |
| AutoML (ET) | 0.8638  | 0.7915    | 0.9325 | 0.8562   | 0.9187  |
| AutoML (DT) | 0.8614  | 0.7876    | 0.9327 | 0.8541   | 0.9117  |

> Uwaga: Tabela przedstawia najlepsze modele AutoML (drzewiaste).

---

## 4. Wnioski

1. **AutoML znacząco poprawia wyniki w porównaniu do baseline**.  
   - Recall dla klasy opóźnionych lotów wzrósł z 0 do ~0.94.  
   - F1-score również uległo dużej poprawie.  

2. **Modele drzewiaste (RF, ET, DT) najlepiej radzą sobie z tym zadaniem**, zarówno pod względem Recall, jak i F1-score.  

3. **Modele liniowe i klasyczne baseline** nie radzą sobie z problemem wykrywania opóźnionych lotów.  

4. Rekomendowane modele do dalszego użycia: **Random Forest** i **Extra Trees**.

---

## 5. Podsumowanie

Porównanie wyników pokazuje, że AutoML wybiera modele znacznie lepiej dopasowane do zadania predykcji opóźnień lotów niż prosty baseline. Najlepsze modele osiągają wysokie wartości Accuracy, Recall i F1-score, co czyni je odpowiednimi do dalszej implementacji w systemie predykcyjnym.
