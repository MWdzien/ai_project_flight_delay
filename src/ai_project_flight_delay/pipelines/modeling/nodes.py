import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)
from pycaret.classification import (
    setup, compare_models, pull, finalize_model, predict_model
)

RANDOM_SEED = 42

def _compute_classification_metrics(y_true, y_pred, y_proba=None):
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
    }

    if y_proba is not None:
        try:
            metrics["roc_auc"] = float(roc_auc_score(y_true, y_proba[:, 1]))
        except Exception:
            metrics["roc_auc"] = None
    else:
        metrics["roc_auc"] = None

    return metrics

def train_baseline(train_data: pd.DataFrame, val_data: pd.DataFrame):
    X_train = train_data.drop(columns=["is_delayed"])
    y_train = train_data["is_delayed"]

    X_val = val_data.drop(columns=["is_delayed"])
    y_val = val_data["is_delayed"]

    model = DummyClassifier(strategy="most_frequent")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)

    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_val)
    else:
        y_proba = None

    metrics = _compute_classification_metrics(y_val, y_pred, y_proba)

    return model, metrics

def train_automl(train_data: pd.DataFrame, val_data: pd.DataFrame):
    full_data = pd.concat([train_data, val_data], axis=0).reset_index(drop=True)

    setup(
        data=full_data,
        target="is_delayed",
        train_size=len(train_data) / len(full_data),
        session_id=RANDOM_SEED,
        html=False,
        verbose=False
    )

    best_model = compare_models(sort="F1")
    best_model_final = finalize_model(best_model)

    automl_results_df = pull()

    predictions = predict_model(best_model_final, data=val_data)
    y_true = val_data["is_delayed"]
    y_pred = predictions["prediction_label"]

    if "prediction_score" in predictions.columns:
        y_proba = np.vstack([1 - predictions["prediction_score"],
                             predictions["prediction_score"]]).T
    else:
        y_proba = None

    metrics = _compute_classification_metrics(y_true, y_pred, y_proba)

    return best_model_final, metrics, automl_results_df

def evaluate_models(baseline_metrics: dict, automl_metrics: dict):
    return {
        "baseline": baseline_metrics,
        "automl": automl_metrics
    }

