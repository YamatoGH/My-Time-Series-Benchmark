# My-Time-Series-Benchmark

STEP1 として、時系列モデルの最小ベンチマーク環境を構築しました。  
Naive / ARIMA / LSTM を共通インターフェースで動かし、MAE/RMSE/MAPE/SMAPE/R² で評価、Tableau 連携用の CSV を出力します。

## ディレクトリ構成
```
mtsp/
  models/             # baseline, statistical, dl の各モデル
  evaluation/basic/   # MAE, RMSE, MAPE, SMAPE, R2
  utils/              # BaseModel, BaseMetric, DatasetLoader
  data/
    raw/daily_sales.csv      # サンプル日次売上データ
    processed/               # 生成される forecast.csv / metrics.csv
    metadata/daily_sales.json
  pipelines/          # run_models_step1.py / evaluate_step1.py / export_tableau_step1.py
  exports_for_tableau/
    forecasts/        # Tableau 受け渡し用 forecast.csv
    metrics/          # Tableau 受け渡し用 metrics.csv
requirements.txt      # 依存パッケージ
```

## セットアップ
1. Python 3.10+ を推奨（TensorFlow が必要なため仮想環境推奨）。
2. 依存をインストール  
   ```
   pip install -r requirements.txt
   ```
   ※ TensorFlow/ARIMA が不要なら該当行を削っても動作します（Naive のみ実行）。

## パイプラインの流れ (STEP1)
1) 予測生成  
```
python -m mtsp.pipelines.run_models_step1
```
`mtsp/data/processed/forecast.csv` が作成されます（モデル別に予測値・実測値を格納）。

2) 評価計算  
```
python -m mtsp.pipelines.evaluate_step1
```
`mtsp/data/processed/metrics.csv` に 5 指標のスコアを保存。

3) Tableau 用エクスポート  
```
python -m mtsp.pipelines.export_tableau_step1
```
`mtsp/exports_for_tableau/forecasts/forecast.csv` と  
`mtsp/exports_for_tableau/metrics/metrics.csv` を配置します。

## データ
- `mtsp/data/raw/daily_sales.csv`  
  日次売上のサンプルデータ（200日分）。気温と降雨フラグを外生変数として含みます。
- `mtsp/data/metadata/daily_sales.json`  
  目的変数名・タイムスタンプ列・頻度・外生変数を定義。

## 今後の拡張候補 (STEP2 以降)
- モデル追加: Prophet / LightGBM / GRU など
- 評価追加: 残差検定・horizon 別精度・Diebold-Mariano 検定
- データセット追加: us_demand / visitors など
