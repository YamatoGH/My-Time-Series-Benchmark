# プロジェクトスナップショット（My-Time-Series-Benchmark）

## 目的と現状
- MTSB は時系列予測モデルを統一インターフェースで評価・比較する個人向けベンチマーク基盤。
- STEP1 ではベースラインから簡易ディープラーニングまでのモデルと、基本的な誤差指標を揃え済み。
- Tableau などの可視化ツールで利用できる形で予測値と指標をエクスポート可能。

## ディレクトリ構成（主要部）
```text
My-Time-Series-Benchmark/
├─ analysis/                  # モデル別・指標別の簡易メモ
├─ exports_for_tableau/       # Tableau 用の出力 (forecast.csv, metrics.csv あり)
├─ mtsb/                      # コアパッケージ
│  ├─ data/
│  │  ├─ raw/                 # 生データ (daily_sales.csv)
│  │  └─ metadata/            # メタデータ (daily_sales.json)
│  ├─ evaluation/basic/       # MAE, RMSE, MAPE, SMAPE, R2 の実装
│  ├─ models/                 # baseline / statistical / dl モデル群
│  ├─ pipelines/              # STEP1 の実行スクリプト一式
│  ├─ utils/                  # BaseModel, BaseMetric, DatasetLoader など
│  └─ notebooks/              # 検証用ノートブック (naive.ipynb)
├─ first_plot.md              # 可視化メモ
├─ README.md                  # プロジェクト概要
├─ requirements.txt           # 依存関係 (pandas, numpy, statsmodels, tensorflow-cpu)
└─ time_series_evaluation.md  # 評価方針ドキュメント
```

## データセット
- `mtsb/data/raw/daily_sales.csv`（気温・降雨フラグを含む日次売上データ）。
- メタデータは `mtsb/data/metadata/daily_sales.json` に定義。
- `DatasetLoader` が欠損補完、頻度設定、学習/テスト分割（`horizon` 指定）を担当。

## モデルと指標（STEP1）
- モデル: `NaiveModel`（直近値保持）、`ARIMAModel`（statsmodels 依存）、`LSTMSimpleModel`（tensorflow 依存、単層 LSTM）。
- 指標: MAE, RMSE, MAPE, SMAPE, R2 を `mtsb/evaluation/basic/` で提供。
- 共通の基底クラスは `mtsb/utils/base_model.py` と `mtsb/utils/base_metric.py`。

## 実行フローと出力
1. `python mtsb/pipelines/run_models_step1.py`  
   - データ読込→学習→30 ステップ先まで予測を作成し、`mtsb/data/processed/forecast.csv` に保存。
2. `python mtsb/pipelines/evaluate_step1.py`  
   - 予測と実績から上記指標を計算し、`mtsb/data/processed/metrics.csv` に保存。
3. `python mtsb/pipelines/export_tableau_step1.py`  
   - Tableau で使いやすいよう `exports_for_tableau/forecasts/forecast.csv` と `exports_for_tableau/metrics/metrics.csv` に複製。

備考: 現在リポジトリ直下の `exports_for_tableau/` にも `forecast.csv` と `metrics.csv` が存在し、直近の出力を確認可能。
