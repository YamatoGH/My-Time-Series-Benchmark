# 📘 Baseline Model Notebook Template（naive.ipynb 完全準拠）

このテンプレートは、`mtsb/notebooks/` 直下で実行する Jupyter Notebook を想定しています。  
**パス・import・出力先は必ずこのテンプレ通りにしてください。**

---

## ✅ 前提・置き換え用プレースホルダ

- `{MODEL_KEY}`: モデル識別子（例: `"naive"`, `"seasonal_naive"`, `"drift"`, `"moving_average"`）
- `{MODEL_MODULE}`: `models.baseline` 以下のモジュール名  
  - 例: `"naive"`, `"seasonal_naive"`, `"drift"`, `"moving_average"`
- `{MODEL_CLASS}`: モデルクラス名  
  - 例: `NaiveModel`, `SeasonalNaiveModel`, `DriftModel`, `MovingAverageModel`

---

## 🔧 セル0：プロジェクトルートを sys.path に追加

```python
import sys
import os

# 現在: mtsb/notebooks
# 1つ上は: mtsb/
PROJECT_ROOT = os.path.abspath("..")
sys.path.append(PROJECT_ROOT)

print("Added to sys.path:", PROJECT_ROOT)
📂 セル1：データ読み込み
python
コードをコピーする
# データ読み込み
import pandas as pd

# mtsb/notebooks から見て 1つ上の ../data/raw/
df = pd.read_csv("../data/raw/daily_sales.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

y = df["sales"]

# 30日先予測（ベースモデルは未来特徴量を使わないためこれでOK）
horizon = 30
train = y.iloc[:-horizon]
test = y.iloc[-horizon:]
🤖 セル2：ベースラインモデルの適用
python
コードをコピーする
# ベースラインモデルを適用
from models.baseline.{MODEL_MODULE} import {MODEL_CLASS}

model = {MODEL_CLASS}(freq="D")  # freq は日次データの例
model.fit(train)

# NOTE: naive.ipynb と同じく .forecast ではなく .y_pred を呼び出す前提
y_pred = model.y_pred(horizon)
⚠ モデル側で y_pred(horizon) を実装しておくこと。
既存の NaiveModel と同じインターフェースに揃える。

📊 セル3：評価指標の計算
python
コードをコピーする
from evaluation.basic.mae import MAE
from evaluation.basic.rmse import RMSE
from evaluation.basic.mape import MAPE
from evaluation.basic.smape import SMAPE
from evaluation.basic.r2 import R2

metrics = {
    "mae": MAE().compute(test, y_pred),
    "rmse": RMSE().compute(test, y_pred),
    "mape": MAPE().compute(test, y_pred),
    "smape": SMAPE().compute(test, y_pred),
    "r2": R2().compute(test, y_pred),
}

print(metrics)
💾 セル4：予測結果を CSV で保存
python
コードをコピーする
# 予測結果をCSVで保存
forecast_df = pd.DataFrame({
    "date": y_pred.index,
    "actual": test.values,
    "forecast": y_pred.values,
    "model": "{MODEL_KEY}",
})

forecast_df.to_csv(f"../../exports_for_tableau/{MODEL_KEY}_forecast.csv", index=False)


💾 セル5：評価指標を CSV で保存
python
コードをコピーする
# 評価指標をCSVで保存
metrics_df = pd.DataFrame([{
    "model": "{MODEL_KEY}",
    **metrics,
}])

metrics_df.to_csv(f"../../exports_for_tableau/{MODEL_KEY}_metrics.csv", index=False)
