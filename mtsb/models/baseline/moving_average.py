from __future__ import annotations

import pandas as pd

from utils.base_model import BaseModel


class MovingAverageModel(BaseModel):
    """Simple moving average baseline model using the last N observations."""

    def __init__(self, freq: str, window: int):
        super().__init__("moving_average", freq)
        self.window = window
        self._train_series: pd.Series | None = None
        self._last_timestamp: pd.Timestamp | None = None

    def fit(self, y: pd.Series, exogenous: pd.DataFrame | None = None) -> None:
        if len(y) < self.window:
            raise ValueError(f"Not enough observations for window size {self.window}")

        self._train_series = y.copy()
        self._last_timestamp = y.index[-1]

    def forecast(
        self,
        horizon: int,
        exogenous_future: pd.DataFrame | None = None
    ) -> pd.Series:

        if self._train_series is None or self._last_timestamp is None:
            raise RuntimeError("Call fit before forecast")

        # 未来インデックス生成（naive.py と完全一致）
        future_index = self._build_future_index(self._last_timestamp, horizon)

        # 直近 window 個分の平均値
        mean_value = float(self._train_series.iloc[-self.window :].mean())

        values = [mean_value] * horizon

        return pd.Series(values, index=future_index, name=self.name)
