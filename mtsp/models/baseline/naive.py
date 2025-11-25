from __future__ import annotations

import pandas as pd

from mtsp.utils.base_model import BaseModel


class NaiveModel(BaseModel):
    """Simple baseline that repeats the last observed value."""

    def __init__(self, freq: str):
        super().__init__("naive", freq)
        self._last_value: float | None = None
        self._last_timestamp: pd.Timestamp | None = None

    def fit(self, y: pd.Series, exogenous: pd.DataFrame | None = None) -> None:
        if len(y) == 0:
            raise ValueError("Training series is empty")
        self._last_value = float(y.iloc[-1])
        self._last_timestamp = y.index[-1]

    def forecast(
        self, horizon: int, exogenous_future: pd.DataFrame | None = None
    ) -> pd.Series:
        if self._last_value is None or self._last_timestamp is None:
            raise RuntimeError("Call fit before forecast")

        future_index = self._build_future_index(self._last_timestamp, horizon)
        return pd.Series(
            [self._last_value] * horizon,
            index=future_index,
            name=self.name,
        )
