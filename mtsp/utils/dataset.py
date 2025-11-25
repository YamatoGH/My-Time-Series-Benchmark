from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd


class DatasetLoader:
    """Lightweight loader for STEP1 datasets."""

    def __init__(self, data_path: str, metadata_path: str):
        self.data_path = Path(data_path)
        self.metadata_path = Path(metadata_path)

    def load(self) -> Tuple[pd.Series, Optional[pd.DataFrame], dict]:
        metadata = self._load_metadata()
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        df = pd.read_csv(
            self.data_path,
            parse_dates=[metadata["timestamp_column"]],
        )
        timestamp_col = metadata["timestamp_column"]
        target_col = metadata["target_column"]
        freq = metadata.get("frequency")
        exog_cols = metadata.get("exogenous_columns") or []

        df = df.sort_values(timestamp_col)
        df = df.set_index(timestamp_col)
        if freq:
            df = df.asfreq(freq)
        df = df.interpolate(method="time").fillna(method="bfill").fillna(method="ffill")

        target = df[target_col]
        exog = df[exog_cols] if exog_cols else None

        if not freq:
            inferred = pd.infer_freq(target.index)
            if inferred:
                metadata["frequency"] = inferred

        return target, exog, metadata

    def train_test_split(
        self, horizon: int
    ) -> Tuple[pd.Series, pd.Series, Optional[pd.DataFrame], Optional[pd.DataFrame], dict]:
        if horizon <= 0:
            raise ValueError("horizon must be positive")

        y, exog, metadata = self.load()
        if horizon >= len(y):
            raise ValueError("horizon must be smaller than the number of observations")

        train_y = y.iloc[:-horizon]
        test_y = y.iloc[-horizon:]

        if exog is not None:
            train_exog = exog.iloc[:-horizon]
            test_exog = exog.iloc[-horizon:]
        else:
            train_exog = None
            test_exog = None

        return train_y, test_y, train_exog, test_exog, metadata

    def _load_metadata(self) -> dict:
        if not self.metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_path}")
        with self.metadata_path.open("r", encoding="utf-8") as f:
            return json.load(f)
