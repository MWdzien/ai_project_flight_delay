import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
from pathlib import Path

log = logging.getLogger(__name__)

OUTPUT_DIR = Path("data/02_intermediate/eda_outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_raw_data(raw_data) -> pd.DataFrame:
    log.info("Ładowanie danych surowych")
    return raw_data 

def basic_statistics(df: pd.DataFrame) -> dict:
    log.info("Generowanie podstawowych statystyk")
    stats = {
        "shape": df.shape,
        "dtypes": df.dtypes.to_dict(),
        "describe": df.describe(include='all').to_dict()
    }
    (OUTPUT_DIR / "basic_stats.csv").write_text(pd.DataFrame(df.describe(include='all')).to_csv())
    return stats

def missing_and_outliers(df: pd.DataFrame) -> dict:
    log.info("Analiza braków i wartości odstających")
    missing = df.isna().sum().sort_values(ascending=False)
    numeric = df.select_dtypes(include='number')
    outlier_summary = {}
    for col in numeric.columns:
        q1 = numeric[col].quantile(0.25)
        q3 = numeric[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_count = ((numeric[col] < lower) | (numeric[col] > upper)).sum()
        outlier_summary[col] = int(outlier_count)
    missing.to_csv(OUTPUT_DIR / "missing.csv")
    pd.Series(outlier_summary).to_csv(OUTPUT_DIR / "outliers.csv")
    return {"missing": missing.to_dict(), "outliers": outlier_summary}

def visualize(df: pd.DataFrame) -> dict:
    log.info("Tworzenie wykresów - histogramy, boxploty, heatmapa korelacji")
    res = {}
    numeric = df.select_dtypes(include='number').columns.tolist()
    cat = df.select_dtypes(include='object').columns.tolist()

    for col in numeric[:6]:
        plt.figure()
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f"Histogram: {col}")
        filename = OUTPUT_DIR / f"hist_{col}.png"
        plt.savefig(filename)
        plt.close()
        res[f"hist_{col}"] = str(filename)

    for col in numeric[:6]:
        plt.figure()
        sns.boxplot(x=df[col])
        plt.title(f"Boxplot: {col}")
        filename = OUTPUT_DIR / f"box_{col}.png"
        plt.savefig(filename)
        plt.close()
        res[f"box_{col}"] = str(filename)

    if len(numeric) > 1:
        plt.figure(figsize=(10,8))
        corr = df[numeric].corr()
        sns.heatmap(corr, annot=False)
        filename = OUTPUT_DIR / "corr_heatmap.png"
        plt.savefig(filename)
        plt.close()
        res["corr_heatmap"] = str(filename)

    plt.figure()
    msno.matrix(df.sample(n=min(2000, len(df))))  # próbka dla wydajności
    filename = OUTPUT_DIR / "missing_matrix.png"
    plt.savefig(filename)
    plt.close()
    res["missing_matrix"] = str(filename)

    return res
