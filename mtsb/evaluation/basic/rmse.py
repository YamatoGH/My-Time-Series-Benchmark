from __future__ import annotations

import numpy as np
import pandas as pd

from utils.base_metric import BaseMetric


class RMSE(BaseMetric):
    name = "rmse"

    def compute(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        return float(np.sqrt(((y_true - y_pred) ** 2).mean()))
