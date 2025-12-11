from kedro.pipeline import Pipeline, node
from .nodes import train_baseline, train_automl, evaluate_models, train_best_model

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(train_baseline, ["train_data", "val_data"], ["baseline_model", "baseline_metrics"]),
            node(train_automl, ["train_data", "val_data"], ["automl_model", "automl_metrics", "automl_results"]),
            node(func=train_best_model,inputs=["train_data", "val_data"],outputs=["best_model", "best_model_metrics"],name="train_best_model"),
            node(evaluate_models, ["baseline_metrics", "automl_metrics"], "model_comparison"),
        ]
    )
