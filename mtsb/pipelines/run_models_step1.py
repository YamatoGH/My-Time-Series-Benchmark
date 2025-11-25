from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from mtsb.models.baseline.naive import NaiveModel
from mtsb.models.dl.lstm_simple import LSTMSimpleModel
from mtsb.models.statistical.arima import ARIMAModel
from mtsb.utils.dataset import DatasetLoader

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data/raw/daily_sales.csv"
METADATA_PATH = ROOT / "data/metadata/daily_sales.json"
PROCESSED_DIR = ROOT / "data/processed"
FORECAST_PATH = PROCESSED_DIR / "forecast.csv"
HORIZON = 30


def build_models(freq: str) -> List:
    models = []
    for model_ctor in (
        lambda: NaiveModel(freq),
        lambda: ARIMAModel(freq),
        lambda: LSTMSimpleModel(freq),
    ):
        try:
            models.append(model_ctor())
        except ImportError as exc:
            print(f"Skipping model because dependency is missing: {exc}")
    return models


def run() -> pd.DataFrame:
    loader = DatasetLoader(DATA_PATH, METADATA_PATH)
    train_y, test_y, train_exog, test_exog, metadata = loader.train_test_split(
        horizon=HORIZON
    )
    freq = metadata["frequency"]

    forecasts = []
    for model in build_models(freq):
        print(f"Training {model.name}...")
        model.fit(train_y, train_exog)
        pred = model.forecast(HORIZON, exogenous_future=test_exog)
        aligned_actual = test_y.reindex(pred.index)
        forecasts.append(
            pd.DataFrame(
                {
                    "date": pred.index,
                    "model": model.name,
                    "forecast": pred.values,
                    "actual": aligned_actual.values,
                }
            )
        )

    forecast_df = pd.concat(forecasts, ignore_index=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    forecast_df.to_csv(FORECAST_PATH, index=False)
    print(f"Saved forecasts to {FORECAST_PATH}")
    return forecast_df


if __name__ == "__main__":
    run()
