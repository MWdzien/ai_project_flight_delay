from kedro.pipeline import Pipeline, node
from .nodes import (
    cross_validate_model,
    evaluate_on_test,
    analyze_errors,
    analyze_shap_values,
    log_to_mlflow,
    save_version_info
)

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=cross_validate_model,
            inputs=["best_model", "train_data"],
            outputs="cv_results",
            name="cross_validation"
        ),
        node(
            func=evaluate_on_test,
            inputs=["best_model", "test_data"],
            outputs="test_metrics",
            name="evaluate_test"
        ),
        node(
            func=analyze_errors,
            inputs=["best_model", "test_data"],
            outputs="feature_importances",
            name="analyze_errors"
        ),
        node(
            func=analyze_shap_values,
            inputs=["best_model", "test_data"],
            outputs="shap_done",
            name="shap_analysis"
        ),
        node(
            func=log_to_mlflow,
            inputs=["best_model", "test_metrics", "cv_results", "params:model_params"],
            outputs="mlflow_info",
            name="log_mlflow"
        ),
        node(
            func=save_version_info,
            inputs="test_metrics",
            outputs="version_info",
            name="save_version"
        )
    ])