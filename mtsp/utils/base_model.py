from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd
from pandas.tseries.frequencies import to_offset


class BaseModel(ABC):
    """Common interface for time-series models used in the benchmark."""

    def __init__(self, name: str, freq: str):
        self.name = name
        self.freq = freq

    @abstractmethod
    def fit(self, y: pd.Series, exogenous: Optional[pd.DataFrame] = None) -> None:
        """Train the model on a target series and optional exogenous features."""

    @abstractmethod
    def forecast(
        self, horizon: int, exogenous_future: Optional[pd.DataFrame] = None
    ) -> pd.Series:
        """Predict the next `horizon` steps."""

    def _build_future_index(self, last_timestamp: pd.Timestamp, horizon: int) -> pd.DatetimeIndex:
        """Construct a datetime index for future predictions."""
        offset = to_offset(self.freq)
        return pd.date_range(start=last_timestamp + offset, periods=horizon, freq=offset)
