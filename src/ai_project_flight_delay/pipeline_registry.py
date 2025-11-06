"""Project pipelines."""
from __future__ import annotations

from kedro.pipeline import Pipeline
from ai_project_flight_delay.pipelines import eda_pipeline


def register_pipelines() -> dict[str, Pipeline]:
    eda = eda_pipeline.create_pipeline()

    return {
        "__default__": eda,
        "eda": eda,
    }
