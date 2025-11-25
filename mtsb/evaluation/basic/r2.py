from __future__ import annotations

import numpy as np
import pandas as pd

from mtsb.utils.base_metric import BaseMetric


class R2(BaseMetric):
    name = "r2"

    def compute(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        y_true_mean = y_true.mean()
        ss_total = ((y_true - y_true_mean) ** 2).sum()
        ss_res = ((y_true - y_pred) ** 2).sum()
        if ss_total == 0:
            return float("nan")
        return float(1 - ss_res / ss_total)
