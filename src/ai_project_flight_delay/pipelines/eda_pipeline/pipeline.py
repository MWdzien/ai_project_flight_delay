from kedro.pipeline import Pipeline, node
from .nodes import load_raw_data, basic_statistics, missing_and_outliers, visualize, save_report

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(func=load_raw_data, inputs="raw_data", outputs="df_raw"),
            node(func=basic_statistics, inputs="df_raw", outputs="stats"),
            node(func=missing_and_outliers, inputs="df_raw", outputs="missing_outliers"),
            node(func=visualize, inputs="df_raw", outputs="visuals"),
            node(func=save_report, inputs=["stats","missing_outliers","visuals"], outputs="eda_report_path"),
        ]
    )
