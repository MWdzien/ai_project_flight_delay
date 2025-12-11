"""
DAG dla projektu Kedro - Flight Delay Prediction
Używa osobnego środowiska venv z Pythonem 3.11 dla kompatybilności z PyCaret
"""
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Ścieżki - ZMIEŃ NA SWOJE!
PROJECT_PATH = "/Users/I760554/pjatk/org/ai_project_flight_delay"
VENV_PYTHON = f"{PROJECT_PATH}/venv/bin/python"  # Python 3.11 z venv Kedro

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="kedro_flight_delay_pipeline",
    default_args=default_args,
    description="ETL + ML Pipeline dla przewidywania opóźnień lotów",
    schedule_interval=None,  # Manualne uruchamianie
    catchup=False,
    tags=["kedro", "mlops", "flight-delay"],
) as dag:

    # Task 1: EDA Pipeline
    eda_task = BashOperator(
        task_id="eda_pipeline",
        bash_command=f"""
        cd {PROJECT_PATH} && \
        {VENV_PYTHON} -m kedro run --pipeline=eda
        """,
    )

    # Task 2: Preprocessing Pipeline
    preprocessing_task = BashOperator(
        task_id="preprocessing_pipeline",
        bash_command=f"""
        cd {PROJECT_PATH} && \
        {VENV_PYTHON} -m kedro run --pipeline=preprocessing
        """,
    )

    # Task 3: Modeling Pipeline
    modeling_task = BashOperator(
        task_id="modeling_pipeline",
        bash_command=f"""
        cd {PROJECT_PATH} && \
        {VENV_PYTHON} -m kedro run --pipeline=modeling
        """,
    )

    # Task 4: Evaluation Pipeline
    evaluation_task = BashOperator(
        task_id="evaluation_pipeline",
        bash_command=f"""
        cd {PROJECT_PATH} && \
        {VENV_PYTHON} -m kedro run --pipeline=evaluation
        """,
    )

    # Definiowanie zależności (kolejność wykonywania)
    eda_task >> preprocessing_task >> modeling_task >> evaluation_task