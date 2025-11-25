from __future__ import annotations

from pathlib import Path

import pandas as pd

from mtsb.evaluation.basic.mae import MAE
from mtsb.evaluation.basic.mape import MAPE
from mtsb.evaluation.basic.r2 import R2
from mtsb.evaluation.basic.rmse import RMSE
from mtsb.evaluation.basic.smape import SMAPE

ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT / "data/processed"
FORECAST_PATH = PROCESSED_DIR / "forecast.csv"
METRICS_PATH = PROCESSED_DIR / "metrics.csv"


def evaluate() -> pd.DataFrame:
    if not FORECAST_PATH.exists():
        raise FileNotFoundError(f"Forecast file not found: {FORECAST_PATH}")

    df = pd.read_csv(FORECAST_PATH, parse_dates=["date"])
    metrics = [MAE(), RMSE(), MAPE(), SMAPE(), R2()]

    rows = []
    for model_name, group in df.groupby("model"):
        y_true = group["actual"]
        y_pred = group["forecast"]
        for metric in metrics:
            score = metric.compute(y_true, y_pred)
            rows.append({"model": model_name, "metric": metric.name, "value": score})

    metrics_df = pd.DataFrame(rows)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    metrics_df.to_csv(METRICS_PATH, index=False)
    print(f"Saved metrics to {METRICS_PATH}")
    return metrics_df


if __name__ == "__main__":
    evaluate()
