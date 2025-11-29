# src/tests/pipelines/preprocessing/test_nodes.py
import pandas as pd
import numpy as np
from ai_project_flight_delay.pipelines.preprocessing.nodes import clean_data, scale_data, split_data

def make_small_df():
    data = {
        "year": [2024, 2024, 2024, 2024],
        "month": [1, 1, 2, 2],
        "day_of_month": [1, 2, 3, 4],
        "dep_time": [1325.0, 2400.0, np.nan, 730.0],
        "wheels_off": [1335.0, np.nan, 900.0, 745.0],
        "wheels_on": [1450.0, 1500.0, 1015.0, np.nan],
        "taxi_out": [10, 20, 15, 12],
        "taxi_in": [5, 7, 6, np.nan],
        "air_time": [60, 90, 30, 120],
        "distance": [300, 600, 150, 800],
        "late_aircraft_delay": [0, 20, 5, 30],
        "origin": ["ATL","LAX","ATL","JFK"],
    }
    return pd.DataFrame(data)

def test_clean_data_not_empty():
    df = make_small_df()
    out = clean_data(df)
    assert out.shape[0] > 0
    assert "is_delayed" in out.columns

def test_scale_mean_std():
    df = clean_data(make_small_df())
    scaled = scale_data(df, scaler_name="standard")
    num_cols = scaled.select_dtypes(include=["float32","float64","int32","int64"]).columns
    if "is_delayed" in num_cols:
        num_cols = num_cols.drop("is_delayed")
    means = scaled[num_cols].mean().abs()
    assert (means < 1.0).all()

def test_split_ratios():
    df = clean_data(make_small_df())
    scaled = scale_data(df)
    tr, va, te = split_data(scaled, train_size=0.5, val_size=0.25, test_size=0.25, random_state=1)
    total = tr.shape[0] + va.shape[0] + te.shape[0]
    assert total == scaled.shape[0]
    assert tr.shape[0] == 2 
