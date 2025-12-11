import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

from sklearn.model_selection import cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix, classification_report
)
import mlflow
import mlflow.sklearn

# walidacja krzyzowa modelu
def cross_validate_model(model, train_data: pd.DataFrame):
    X_train = train_data.drop(columns=["is_delayed"])
    y_train = train_data["is_delayed"]
    
    cv_scores = {
        "accuracy": cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy'),
        "precision": cross_val_score(model, X_train, y_train, cv=5, scoring='precision'),
        "recall": cross_val_score(model, X_train, y_train, cv=5, scoring='recall'),
        "f1": cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
    }
    
    cv_results = {
        "accuracy_mean": float(np.mean(cv_scores["accuracy"])),
        "accuracy_std": float(np.std(cv_scores["accuracy"])),
        "precision_mean": float(np.mean(cv_scores["precision"])),
        "precision_std": float(np.std(cv_scores["precision"])),
        "recall_mean": float(np.mean(cv_scores["recall"])),
        "recall_std": float(np.std(cv_scores["recall"])),
        "f1_mean": float(np.mean(cv_scores["f1"])),
        "f1_std": float(np.std(cv_scores["f1"]))
    }
    
    return cv_results

# Ocena modelu na zbiorze testowym
def evaluate_on_test(model, test_data: pd.DataFrame):
    X_test = test_data.drop(columns=["is_delayed"])
    y_test = test_data["is_delayed"]
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)
    
    test_metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_proba[:, 1]))
    }
    
    return test_metrics

# Analiza błędów
def analyze_errors(model, test_data: pd.DataFrame):
    X_test = test_data.drop(columns=["is_delayed"])
    y_test = test_data["is_delayed"]
    
    y_pred = model.predict(X_test)
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Not Delayed', 'Delayed'],
                yticklabels=['Not Delayed', 'Delayed'])
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    Path("docs/plots").mkdir(parents=True, exist_ok=True)
    plt.savefig("docs/plots/confusion_matrix.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Feature Importance
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feature_names = X_test.columns
        
        feature_importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(10, 6))
        plt.barh(feature_importance_df['feature'][:10], 
                 feature_importance_df['importance'][:10])
        plt.xlabel('Importance')
        plt.title('Top 10 Feature Importances')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig("docs/plots/feature_importance.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return feature_importance_df.to_dict('records')
    
    return None

def analyze_shap_values(model, test_data: pd.DataFrame):
    """
    Analiza SHAP values (opcjonalna)
    """
    try:
        import shap
        
        X_test = test_data.drop(columns=["is_delayed"])
        
        # Losuj 100 próbek dla szybszego obliczenia SHAP
        X_sample = X_test.sample(n=min(100, len(X_test)), random_state=42)
        
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_sample)
        
        # Dla klasyfikacji binarnej bierzemy wartości dla klasy 1
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, X_sample, show=False)
        plt.tight_layout()
        plt.savefig("docs/plots/shap_summary.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return True
    except Exception as e:
        print(f"SHAP analysis skipped: {e}")
        return False

# logowanie
def log_to_mlflow(model, test_metrics: dict, cv_results: dict, model_params: dict):
    print("⚠️ MLflow logging skipped - not running MLflow server")
    return {"mlflow_status": "skipped"}
    # """
    # Logowanie modelu i metryk do MLflow
    # """
    # import mlflow
    # import os
    
    # # Ustaw tracking URI
    # tracking_uri = 'http://localhost:5000'
    # #tracking_uri = os.path.abspath("./mlruns")
    # mlflow.set_tracking_uri(tracking_uri)
    
    # with mlflow.start_run(run_name="RandomForest_FlightDelay"):
    #     # Log parametrów
    #     mlflow.log_params(model_params)
        
    #     # Log metryk testowych
    #     for key, value in test_metrics.items():
    #         mlflow.log_metric(f"test_{key}", value)
        
    #     # Log metryk z CV
    #     for key, value in cv_results.items():
    #         mlflow.log_metric(f"cv_{key}", value)
        
    #     # ZAKOMENTOWANE - powoduje problemy z artifact URI
    #     # mlflow.sklearn.log_model(model, "model")
        
    #     # Log artefaktów (wykresy)
    #     if Path("docs/plots/confusion_matrix.png").exists():
    #         mlflow.log_artifact("docs/plots/confusion_matrix.png")
    #     if Path("docs/plots/feature_importance.png").exists():
    #         mlflow.log_artifact("docs/plots/feature_importance.png")
    #     if Path("docs/plots/shap_summary.png").exists():
    #         mlflow.log_artifact("docs/plots/shap_summary.png")
        
    #     run_id = mlflow.active_run().info.run_id
    #     print(f"✅ MLflow run completed! Run ID: {run_id}")
        
    # return {"mlflow_run_id": run_id}

def save_version_info(test_metrics: dict):
    """
    Zapisz informacje o wersji modelu
    """
    version_info = {
        "timestamp": datetime.now().isoformat(),
        "model_name": "RandomForest",
        "version": "1.0",
        **test_metrics
    }
    
    # Append do CSV
    csv_path = Path("data/08_reporting/model_versions.csv")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    df = pd.DataFrame([version_info])
    
    if csv_path.exists():
        df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_path, index=False)
    
    return version_info