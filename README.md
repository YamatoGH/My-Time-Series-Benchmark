# 📊 MTSB — My Time Series Benchmark  
*A modular, extensible benchmarking platform for time-series forecasting.*  
*時系列予測モデルのためのモジュラー型ベンチマーク基盤*

---

# 🌏 Overview / 概要

**MTSB (My Time Series Benchmark)** は、  
時系列予測モデル・評価指標・データセットを自由に追加しながら、  
統一的な仕組みで **学習・研究・検証・可視化** を行うための  
**個人向け・研究向けのベンチマークプラットフォーム**です。



# 🎯 Goals / 目的

### ✔ Model Benchmarking / モデル比較  
統一APIによって、どんな時系列モデルでも同じ形式で比較できる

### ✔ Metric Benchmarking / 評価指標の統一化  
MAE / RMSE / 残差検定 / Horizon評価 / DM検定 など拡張可能

### ✔ Dataset Benchmarking / 複数データセット対応  
CSV＋metadata のみで新しいデータセットを簡単追加

### ✔ Visualization / 可視化  
Tableau などBIツールへエクスポートし、  
モデル比較のダッシュボードを構築可能

### ✔ Research-ready / 研究向け  
大学院の研究室でも通用する評価レイヤーを持つ

### ✔ Long-term Growth / 長期発展  
Transformer系（PatchTST, TCN）やFoundation Models（TimesFM, Moirai）まで扱える拡張性

---

# 📂 Project Structure（STEP1）/ プロジェクト構成

mtsb/
│
├── models/
│ ├── baseline/
│ │ └── naive.py
│ ├── statistical/
│ │ └── arima.py
│ └── dl/
│ └── lstm_simple.py
│
├── evaluation/
│ └── basic/
│ ├── mae.py
│ ├── rmse.py
│ ├── mape.py
│ ├── smape.py
│ └── r2.py
│
├── data/
│ ├── raw/
│ │ └── daily_sales.csv
│ ├── processed/
│ └── metadata/
│ └── daily_sales.json
│
├── pipelines/
│ ├── run_models_step1.py
│ ├── evaluate_step1.py
│ └── export_tableau_step1.py
│
├── exports_for_tableau/
│ ├── forecasts/
│ └── metrics/
│
└── utils/
├── base_model.py
├── base_metric.py
└── dataset.py

yaml
コードをコピーする

---

# 🧠 Included in STEP1 / STEP1に含まれるもの

## 🔹 Models / モデル
- **Naive（ベースライン）**  
- **ARIMA（統計モデル）**  
- **Simple LSTM（1層の基本構造）**

## 🔹 Evaluation Metrics / 基本評価指標
- MAE  
- RMSE  
- MAPE  
- SMAPE  
- R²  

## 🔹 Dataset / 代表データセット

**daily_sales.csv**（日次売上データ）

```json
{
  "target_column": "sales",
  "timestamp_column": "date",
  "frequency": "D",
  "exogenous_columns": ["temperature", "rain_flag"],
  "description": "Daily sales data with weather features."
}
🔧 How It Works / 動作の仕組み
1️⃣ Data Loading / データ読み込み
Dataset クラスが

日付処理

欠損処理

周期（D/W/M）対応
を行う。

2️⃣ Model Training / モデル学習
BaseModel を継承したモデルを
統一インターフェース (fit, predict) で扱う。

3️⃣ Evaluation / 評価
各評価指標は BaseMetric を継承し、
compute(y_true, y_pred) でスコア計算。

4️⃣ Export to Tableau / Tableau出力
exports_for_tableau/ に

forecasts

metrics
が書き出され、
Tableauダッシュボードで即可視化可能。

