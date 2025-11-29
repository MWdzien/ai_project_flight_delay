from kedro.pipeline import Pipeline, node
from .nodes import clean_data, split_and_scale

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=clean_data,
                inputs="raw_data",
                outputs="clean_data",
                name="clean_data_node",
            ),
            node(
                func=split_and_scale,
                inputs="clean_data",
                outputs=["train_data", "val_data", "test_data"],
                name="split_and_scale_node",
            ),
        ]
    )
