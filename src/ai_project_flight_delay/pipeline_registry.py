"""Project pipelines."""
from __future__ import annotations

from kedro.pipeline import Pipeline
from ai_project_flight_delay.pipelines import eda_pipeline
from ai_project_flight_delay.pipelines import preprocessing as preprocessing_pipeline
from ai_project_flight_delay.pipelines import modeling as modeling_pipeline
from ai_project_flight_delay.pipelines import evaluation as evaluation_pipeline



def register_pipelines() -> dict[str, Pipeline]:
    eda = eda_pipeline.create_pipeline()

    return {
        "__default__": eda,
        "eda": eda,
        "preprocessing": preprocessing_pipeline.create_pipeline(),
        "modeling": modeling_pipeline.create_pipeline(),
        "evaluation": evaluation_pipeline.create_pipeline(),
    }
