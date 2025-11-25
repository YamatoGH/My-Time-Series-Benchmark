from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class BaseMetric(ABC):
    """Common interface for evaluation metrics."""

    name: str

    @abstractmethod
    def compute(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        """Return a scalar score comparing truth vs prediction."""
