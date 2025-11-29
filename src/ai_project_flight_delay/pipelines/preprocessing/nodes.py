import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.utils import resample

logger = logging.getLogger(__name__)

LEAKAGE_COLS = [
    "late_aircraft_delay", "weather_delay",
    "dep_time", "wheels_on", "wheels_off", "taxi_in", "taxi_out", "air_time"
]

CATEGORICAL_COLS = ["origin", "origin_city_name", "origin_state_nm"]

# ==========================================
# 1) CLEANING + TARGET
# ==========================================
def clean_data(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df["is_delayed"] = (df["late_aircraft_delay"] > 15).astype(int)
    cols_to_drop = [c for c in LEAKAGE_COLS + ["fl_date", "cancelled"] if c in df.columns]
    if cols_to_drop:
        logger.info(f"Usuwam kolumny leakujące: {cols_to_drop}")
        df = df.drop(columns=cols_to_drop)
    df = df.dropna(subset=df.columns)
    return df

# ==========================================
# 2) SPLIT + UPSAMPLING + SCALING + ENCODING
# ==========================================
def split_and_scale(df: pd.DataFrame, oversample: bool = True):
    y = df["is_delayed"]
    X = df.drop(columns=["is_delayed"])

    # Podział na train/val/test
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.4, stratify=y, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )

    # =========================
    # Upsampling klasy rzadkiej w train
    # =========================
    if oversample:
        train_df = pd.concat([X_train, y_train], axis=1)
        df_majority = train_df[train_df.is_delayed == 0]
        df_minority = train_df[train_df.is_delayed == 1]

        df_minority_upsampled = resample(
            df_minority,
            replace=True,
            n_samples=len(df_majority),
            random_state=42
        )
        train_df = pd.concat([df_majority, df_minority_upsampled])
        X_train = train_df.drop(columns=["is_delayed"])
        y_train = train_df["is_delayed"]

    # =========================
    # Label encoding kolumn kategorycznych
    # =========================
    le_dict = {}
    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        X_train[col] = le.fit_transform(X_train[col])
        X_val[col] = le.transform(X_val[col])
        X_test[col] = le.transform(X_test[col])
        le_dict[col] = le

    # =========================
    # Skalowanie kolumn numerycznych
    # =========================
    numeric_cols = X_train.select_dtypes(include=[np.number]).columns
    scaler = StandardScaler()
    X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_val[numeric_cols] = scaler.transform(X_val[numeric_cols])
    X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

    # =========================
    # Łączenie X i y w DataFrame
    # =========================
    train_df = X_train.copy()
    train_df["is_delayed"] = y_train
    val_df = X_val.copy()
    val_df["is_delayed"] = y_val
    test_df = X_test.copy()
    test_df["is_delayed"] = y_test

    return train_df, val_df, test_df
