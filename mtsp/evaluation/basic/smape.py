from __future__ import annotations

import numpy as np
import pandas as pd

from mtsp.utils.base_metric import BaseMetric


class SMAPE(BaseMetric):
    name = "smape"

    def compute(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        numerator = (y_pred - y_true).abs()
        denominator = (y_true.abs() + y_pred.abs()) / 2.0
        ratio = numerator / denominator.replace(0, np.nan)
        ratio = ratio.dropna()
        if len(ratio) == 0:
            return float("nan")
        return float((ratio.mean()) * 100.0)
