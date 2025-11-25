from __future__ import annotations

import numpy as np
import pandas as pd

from mtsb.utils.base_metric import BaseMetric


class MAPE(BaseMetric):
    name = "mape"

    def compute(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        denom = y_true.replace(0, np.nan).abs()
        pct_error = ((y_true - y_pred).abs() / denom).dropna()
        if len(pct_error) == 0:
            return float("nan")
        return float(pct_error.mean() * 100.0)
