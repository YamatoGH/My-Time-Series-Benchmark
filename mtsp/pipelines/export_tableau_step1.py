from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT / "data/processed"
FORECAST_INPUT = PROCESSED_DIR / "forecast.csv"
METRICS_INPUT = PROCESSED_DIR / "metrics.csv"
EXPORT_FORECAST_DIR = ROOT / "exports_for_tableau/forecasts"
EXPORT_METRICS_DIR = ROOT / "exports_for_tableau/metrics"


def export() -> None:
    if not FORECAST_INPUT.exists() or not METRICS_INPUT.exists():
        raise FileNotFoundError("Run run_models_step1.py and evaluate_step1.py before exporting.")

    forecast_df = pd.read_csv(FORECAST_INPUT, parse_dates=["date"])
    metrics_df = pd.read_csv(METRICS_INPUT)

    EXPORT_FORECAST_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_METRICS_DIR.mkdir(parents=True, exist_ok=True)

    forecast_out = EXPORT_FORECAST_DIR / "forecast.csv"
    metrics_out = EXPORT_METRICS_DIR / "metrics.csv"

    forecast_df.to_csv(forecast_out, index=False)
    metrics_df.to_csv(metrics_out, index=False)

    print(f"Exported forecast to {forecast_out}")
    print(f"Exported metrics to {metrics_out}")


if __name__ == "__main__":
    export()
