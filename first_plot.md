基本構築計画書
#️⃣ STEP1：基本モデル × 基本評価 × 代表データ構築計画

この文書は、時系列ベンチマーク基盤（MTSP）の 最小構成 を構築するための設計書です。

まずは以下の3つを作り、
「最小限だが完成したベンチマーク環境」 を成立させます：

基本モデル（3つ）

基本評価指標（5つ）

代表データセット（1つ）

これだけで
モデル比較 → 評価 → Tableau可視化
までの流れが完成します。

🎯 目的（STEP1の到達点）

最低限のモデルでベンチマークが動く

統一インターフェースを確立する

シンプルな評価関数を揃える

データを読み込み → 前処理 → モデルに渡すフローを確立

Tableauに渡す用の forecast.csv / metrics.csv を出力できる

ここで構築した基盤に、今後モデルや評価関数を「無限に追加」していく。

📁 ディレクトリ構成（STEP1最小版）
mtsp/
│
├── models/
│   ├── baseline/
│   │   └── naive.py
│   ├── statistical/
│   │   └── arima.py
│   └── dl/
│       └── lstm_simple.py
│
├── evaluation/
│   └── basic/
│       ├── mae.py
│       ├── rmse.py
│       ├── mape.py
│       ├── smape.py
│       └── r2.py
│
├── data/
│   ├── raw/
│   │   └── daily_sales.csv
│   ├── processed/
│   └── metadata/
│       └── daily_sales.json
│
├── pipelines/
│   ├── run_models_step1.py
│   ├── evaluate_step1.py
│   └── export_tableau_step1.py
│
├── exports_for_tableau/
│   ├── forecasts/
│   └── metrics/
│
└── utils/
    ├── base_model.py
    ├── base_metric.py
    └── dataset.py

🧩 1. 基本モデル（STEP1で実装）

最低限の比較ができる 3モデル を実装します。

🟦 ① Naive Model（ベースライン）

今日の予測 = 昨日の値

全モデル比較の土台

1行で動く

役割：
「最低限これより良ければ OK」という基準を作る。

🟧 ② ARIMA（統計モデルの基礎）

SARIMA ではなく、まずは単純 ARIMA

model.fit → model.forecast(steps=horizon)

役割：
短期予測で強いモデルを作る。

🟥 ③ LSTM（深層学習の最小構成）

Keras を使った 1-Layer LSTM

複雑なアーキテクチャは使わない

最低限の深層学習モデル

役割：
DL系モデルの“入口”として評価可能にする。

🧠 2. 基本評価指標（STEP1で実装）

「一般的なモデル比較」で必須の 5つだけ 使います。

✔ MAE（平均絶対誤差）

シンプルで外れ値に比較的強い。

✔ RMSE（平方平均二乗誤差）

大きな誤差を厳しく評価。

✔ MAPE（平均絶対百分率誤差）

実務でよく使われる（ただし0に弱い）。

✔ SMAPE（対称MAPE）

MAPEより実務で安定する。

✔ R²（決定係数）

説明力を見る。

→ STEP1ではこれだけで十分。
　STEP2以降に、残差検定・horizon評価・DM検定などを追加する。

🧾 3. 代表データセット（STEP1構築）

まずは 日次売上データ（daily_sales.csv） を代表データとして採用。

📄 daily_sales.csv（例）
date,sales,temperature,rain_flag
2023-01-01,120,5,0
2023-01-02,98,7,1
2023-01-03,110,6,0
...

📑 metadata/daily_sales.json
{
  "target_column": "sales",
  "timestamp_column": "date",
  "frequency": "D",
  "exogenous_columns": ["temperature", "rain_flag"],
  "description": "Daily sales data with weather features."
}

🔧 4. データ読み込み用 DatasetLoader（STEP1版）

基本型だけ先に作成：

日付を index に変換

frequency を合わせる

欠損を簡易処理

🚀 5. STEP1パイプラインの流れ
🔹 run_models_step1.py

データを読み込む

全モデル（Naive / ARIMA / LSTM）を fit

horizon=30 の予測を生成

forecast.csv に書き出し

🔹 evaluate_step1.py

5つの評価関数（MAE/RMSE/...）を適用

結果を metrics.csv に書き出す

🔹 export_tableau_step1.py

forecast.csv と metrics.csv を整形

Tableau用フォルダに配置

※ Tableau側では
「実測 vs 予測」「モデル別RMSE」
のシンプルなダッシュボードを作成。

🧭 6. STEP1 の達成基準（Doneの定義）

以下が動作すれば STEP1 完了：

 Naive / ARIMA / LSTM が学習・予測できる

 評価指標 5つが計算できる

 forecast.csv が生成される

 metrics.csv が生成される

 Tableau でモデル比較が表示できる

 README に STEP1 設計が記載されている

🌱 7. STEP1 の後にすぐ着手すべきもの

STEP2では以下を増やす：

モデル追加（Prophet / LightGBM / GRU）

評価追加（残差検定 / horizon別精度）

データ追加（bus_demand / visitors など）