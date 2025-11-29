from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json

def cross_validate_model(model, X, y):
    """Wykonaj walidację krzyżową"""
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    return {
        'cv_mean': scores.mean(),
        'cv_std': scores.std(),
        'cv_scores': scores.tolist()
    }

def evaluate_on_test_set(model, X_test, y_test):
    """Oceń model na zbiorze testowym"""
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }
    
    return metrics, y_pred

def save_metrics(metrics, filepath):
    """Zapisz metryki do JSON"""
    with open(filepath, 'w') as f:
        json.dump(metrics, f, indent=2)