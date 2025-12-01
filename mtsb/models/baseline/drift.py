from __future__ import annotations

import pandas as pd

from utils.base_model import BaseModel


class DriftModel(BaseModel):
    """Drift baseline model: linear trend extrapolation from first to last value."""

    def __init__(self, freq: str):
        super().__init__("drift", freq)
        self._first_value: float | None = None
        self._last_value: float | None = None
        self._last_timestamp: pd.Timestamp | None = None
        self._n_obs: int | None = None

    def fit(self, y: pd.Series, exogenous: pd.DataFrame | None = None) -> None:
        if len(y) < 2:
            raise ValueError("At least 2 observations are needed for DriftModel.")

        self._first_value = float(y.iloc[0])
        self._last_value  = float(y.iloc[-1])
        self._last_timestamp = y.index[-1]
        self._n_obs = len(y)

    def forecast(
        self,
        horizon: int,
        exogenous_future: pd.DataFrame | None = None
    ) -> pd.Series:

        if (
            self._first_value is None or
            self._last_value is None or
            self._last_timestamp is None or
            self._n_obs is None
        ):
            raise RuntimeError("Call fit before forecast")

        # 未来インデックス
        future_index = self._build_future_index(self._last_timestamp, horizon)

        # drift の傾き
        drift = (self._last_value - self._first_value) / (self._n_obs - 1)

        # h-step ahead forecast
        values = [
            self._last_value + drift * h
            for h in range(1, horizon + 1)
        ]

        return pd.Series(values, index=future_index, name=self.name)
