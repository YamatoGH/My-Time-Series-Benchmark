from __future__ import annotations

import numpy as np
import pandas as pd

from mtsp.utils.base_model import BaseModel

try:
    from tensorflow import keras
except ImportError:  # pragma: no cover - only hit when dependency is missing
    keras = None


class LSTMSimpleModel(BaseModel):
    """Single-layer LSTM for quick benchmarks."""

    def __init__(self, freq: str, lookback: int = 14, epochs: int = 15, batch_size: int = 16):
        super().__init__("lstm_simple", freq)
        self.lookback = lookback
        self.epochs = epochs
        self.batch_size = batch_size
        self.model: keras.Model | None = None
        self._last_timestamp: pd.Timestamp | None = None
        self._last_target_window: np.ndarray | None = None
        self._last_exog_window: np.ndarray | None = None
        self._exog_dim: int = 0

    def _ensure_backend(self) -> None:
        if keras is None:
            raise ImportError(
                "tensorflow is required for LSTMSimpleModel. Install with `pip install tensorflow`."
            )

    def _build_sequences(
        self, series: np.ndarray, exog: np.ndarray | None, lookback: int
    ) -> tuple[np.ndarray, np.ndarray]:
        X, y = [], []
        for idx in range(len(series) - lookback):
            target_window = series[idx : idx + lookback]
            if exog is not None:
                exog_window = exog[idx : idx + lookback]
                window = np.concatenate(
                    [target_window.reshape(lookback, 1), exog_window], axis=1
                )
            else:
                window = target_window.reshape(lookback, 1)
            X.append(window)
            y.append(series[idx + lookback])
        return np.array(X), np.array(y)

    def _prepare_model(self, feature_dim: int) -> keras.Model:
        model = keras.Sequential(
            [
                keras.layers.Input(shape=(self.lookback, feature_dim)),
                keras.layers.LSTM(32),
                keras.layers.Dense(1),
            ]
        )
        model.compile(optimizer="adam", loss="mae")
        return model

    def fit(self, y: pd.Series, exogenous: pd.DataFrame | None = None) -> None:
        self._ensure_backend()
        series = y.astype("float32").values
        exog_values = (
            exogenous.astype("float32").values if exogenous is not None else None
        )
        self._exog_dim = exog_values.shape[1] if exog_values is not None else 0

        lookback = min(self.lookback, len(series) - 1)
        if lookback < 2:
            raise ValueError("Not enough data to train LSTM")
        self.lookback = lookback

        X, y_target = self._build_sequences(series, exog_values, lookback)
        if len(X) == 0:
            raise ValueError("Not enough sliding windows to train LSTM")

        feature_dim = X.shape[2]
        self.model = self._prepare_model(feature_dim)
        self.model.fit(
            X,
            y_target,
            epochs=self.epochs,
            batch_size=self.batch_size,
            verbose=0,
        )

        self._last_target_window = series[-lookback:]
        self._last_exog_window = (
            exog_values[-lookback:] if exog_values is not None else None
        )
        self._last_timestamp = y.index[-1]

    def forecast(
        self, horizon: int, exogenous_future: pd.DataFrame | None = None
    ) -> pd.Series:
        self._ensure_backend()
        if (
            self.model is None
            or self._last_target_window is None
            or self._last_timestamp is None
        ):
            raise RuntimeError("Call fit before forecast")

        future_index = self._build_future_index(self._last_timestamp, horizon)
        target_window = self._last_target_window.copy()

        if self._exog_dim:
            if exogenous_future is None:
                raise ValueError("exogenous_future is required for LSTM forecasts with exogenous inputs")
            exog_future_values = exogenous_future.astype("float32").values
            if len(exog_future_values) < horizon:
                raise ValueError("exogenous_future must include at least `horizon` rows")
            exog_window = self._last_exog_window.copy()
        else:
            exog_future_values = None
            exog_window = None

        preds = []
        for step in range(horizon):
            if exog_window is not None:
                window_features = np.concatenate(
                    [target_window.reshape(self.lookback, 1), exog_window], axis=1
                )
            else:
                window_features = target_window.reshape(self.lookback, 1)

            pred = float(self.model.predict(window_features[np.newaxis, ...], verbose=0)[0, 0])
            preds.append(pred)

            target_window = np.roll(target_window, -1)
            target_window[-1] = pred

            if exog_window is not None:
                exog_window = np.roll(exog_window, -1, axis=0)
                exog_window[-1] = exog_future_values[step]

        return pd.Series(preds, index=future_index, name=self.name)
