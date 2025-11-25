from __future__ import annotations

from typing import Tuple

import pandas as pd

from mtsb.utils.base_model import BaseModel

try:
    from statsmodels.tsa.arima.model import ARIMA
except ImportError:  # pragma: no cover - only hit when dependency is missing
    ARIMA = None


class ARIMAModel(BaseModel):
    """ARIMA wrapper with a minimal interface."""

    def __init__(self, freq: str, order: Tuple[int, int, int] = (1, 1, 0)):
        super().__init__("arima", freq)
        self.order = order
        self._fitted_model = None
        self._last_timestamp: pd.Timestamp | None = None

    def fit(self, y: pd.Series, exogenous: pd.DataFrame | None = None) -> None:
        if ARIMA is None:
            raise ImportError(
                "statsmodels is required for ARIMAModel. Install with `pip install statsmodels`."
            )
        if len(y) < sum(self.order) + 1:
            raise ValueError("Not enough data to fit ARIMA with the configured order")
        self._last_timestamp = y.index[-1]
        self._fitted_model = ARIMA(y, order=self.order, exog=exogenous).fit()

    def forecast(
        self, horizon: int, exogenous_future: pd.DataFrame | None = None
    ) -> pd.Series:
        if self._fitted_model is None or self._last_timestamp is None:
            raise RuntimeError("Call fit before forecast")
        forecast_values = self._fitted_model.forecast(
            steps=horizon, exog=exogenous_future
        )
        forecast_index = self._build_future_index(self._last_timestamp, horizon)
        if isinstance(forecast_values, pd.Series):
            values = forecast_values.values
        else:
            values = forecast_values
        return pd.Series(values, index=forecast_index, name=self.name)
