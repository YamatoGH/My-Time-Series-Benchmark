from __future__ import annotations

import pandas as pd

from utils.base_model import BaseModel


class SeasonalNaiveModel(BaseModel):
    """Seasonal naive baseline that repeats the value from the previous season."""

    def __init__(self, freq: str, seasonal_period: int):
        super().__init__("seasonal_naive", freq)
        self.seasonal_period = seasonal_period
        self._train_series: pd.Series | None = None
        self._last_timestamp: pd.Timestamp | None = None

    def fit(self, y: pd.Series, exogenous: pd.DataFrame | None = None) -> None:
        if len(y) == 0:
            raise ValueError("Training series is empty")

        self._train_series = y.copy()
        self._last_timestamp = y.index[-1]

    def forecast(
        self,
        horizon: int,
        exogenous_future: pd.DataFrame | None = None
    ) -> pd.Series:
        if self._train_series is None or self._last_timestamp is None:
            raise RuntimeError("Call fit before forecast")

        # 未来のインデックスを生成（naive.py と同じ）
        future_index = self._build_future_index(self._last_timestamp, horizon)

        # 過去の seasonal_period 前の値を参照
        values = []
        for h in range(1, horizon + 1):
            # 予測対象となる時点の seasonal_period 前の位置
            # 例：horizon=1 → train[-seasonal_period]
            seasonal_idx = -self.seasonal_period + (h - 1)
            if seasonal_idx < -len(self._train_series):
                # 過去に十分なデータがない場合は、最後の値で埋める
                val = float(self._train_series.iloc[-1])
            else:
                val = float(self._train_series.iloc[seasonal_idx])

            values.append(val)

        return pd.Series(values, index=future_index, name=self.name)
