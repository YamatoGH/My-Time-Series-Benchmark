from __future__ import annotations

import pandas as pd

from mtsp.utils.base_metric import BaseMetric


class MAE(BaseMetric):
    name = "mae"

    def compute(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        return float((y_true - y_pred).abs().mean())
