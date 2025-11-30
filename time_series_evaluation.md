# 📘 時系列予測モデル評価フレームワークドキュメント（My-Time-Series-Benchmark）

このドキュメントは、My-Time-Series-Benchmark プロジェクトにおける全体設計、評価方針、ベースラインからの分析手順、評価基準をまとめたものです。

---

## 🎯 プロジェクト目的

- あらゆる時系列予測モデル（統計・機械学習・深層学習）を公平・一貫して比較するためのベンチマーク基盤を作成。
- 評価指標・データ・可視化・評価手法を統一して管理・拡張可能に。
- Tableau や Python などで再利用しやすい出力を生成。

---

## 📦 ディレクトリ構成（概要）

```
My-Time-Series-Benchmark/
├── analysis/            # Markdownによるモデル・評価・洞察記録
├── mtsb/                # コアロジック（models, evaluation, utils, pipelines）
├── exports_for_tableau/ # 可視化用CSV出力
└── notebooks/           # モデルごとの検証ノートブック
```

---

## 🧠 評価フレームワーク（統一的にやるべきこと）

### 1. モデル出力
- 任意の horizon で予測値（Series）を出力
- `forecast.csv` に保存（date, actual, forecast）

### 2. 評価指標
| 分類 | 指標 | 意味 |
|------|------|------|
| スケール依存 | MAE / RMSE | 基本誤差（対称 / 大誤差重視） |
| スケール非依存 | MAPE / sMAPE | 比較的なパーセント誤差（分母注意） |
| 相対評価 | MASE | Naiveとの比較用（基準として必須） |
| その他 | R2, MAAPE | 分布・堅牢性に応じて任意利用 |

→ すべて `metrics.csv` に記録。

### 3. Horizon別誤差分析
- 各先行ステップ（1日先〜N日先）ごとの誤差を分解
- `horizon_error.csv` に記録

### 4. 残差分析
| やること | 内容 |
|----------|------|
| 残差計算 | y_true - y_pred |
| 自己相関 | ACFでノイズ性をチェック |
| 残差分布 | 平均、歪度、偏差、Q-Qプロットなど |
| バイアス | 系統誤差の有無、曜日/季節ごとの偏り |

→ 結果は `residual.csv`（任意）

### 5. 不確実性（予測区間）
| 指標 | 説明 |
|------|------|
| PICP | 予測区間に真値が含まれる割合（信頼性） |
| MPIW | 予測区間の平均幅（効率性） |
| CRPS / Winkler | 予測分布のスコア（必要に応じて） |

### 6. 安定性・再現性
| 項目 | 内容 |
|------|------|
| Rolling forecast CV | 時系列に沿った検証手法（学習→未来） |
| シード変更再学習 | モデル結果のばらつきを計測（標準偏差） |
| 予測更新変動 | 同じ未来を再予測したときのブレ幅 |

### 7. 統計的比較
| 検定手法 | 内容 |
|----------|------|
| Diebold-Mariano検定 | 2モデルの誤差の有意差判定 |
| MCS（モデル信頼集合） | 有意に劣るモデルを段階的に排除 |

---

## 💼 ビジネス指標による補助評価
| 指標 | 説明 |
|------|------|
| 欠品率 / フィルレート | 予測による供給対応力 |
| 平均在庫高 | 保管コスト影響 |
| 総コストシミュレーション | 売上・利益ベースでの評価 |
| 修正率 | 前回予測からの差（予測安定性） |

→ 必須ではないが、実務導入時は極めて重要。

---

## 🧩 各モデルで共通して行うこと
1. 予測値の出力と保存（forecast.csv）
2. MAE, RMSE, MASE 等を計算（metrics.csv）
3. Horizon別誤差（horizon_error.csv）
4. 残差分析（平均・分布・ACF）
5. 不確実性（可能なら）
6. 可視化（実測 vs 予測, 残差プロット, ヒートマップなど）

---

## 📘 ベースモデル評価だけに必要なこと

| 項目 | 内容 |
|------|------|
| 精度指標 | MAE / RMSE / MASE（基準モデルとして必須） |
| Horizon別誤差 | 後続モデルとの比較軸 |
| 残差平均とACF | 「なにも学習していない」ことの可視化 |
| 可視化 | 折れ線、残差ライン程度でOK |

→ ベースラインは過剰分析しすぎず、比較の起点を明確にする。

---

## 📁 出力ファイルテンプレート

```
exports_for_tableau/
├── forecast.csv         # 日付, 実測, 予測
├── metrics.csv          # MAE, RMSE, MASE, etc.
├── horizon_error.csv    # ステップ別誤差
├── residual.csv         # 残差統計（任意）
└── prediction_intervals.csv  # 予測区間（任意）
```

---

## 📚 参考文献・出典（代表）
- Hyndman & Koehler (2006): Forecast accuracy measures
- Strøm & Gundersen (2024): Horizon-wise forecast evaluation
- Badulescu (2023): Forecast metrics vs inventory performance
- Diebold & Mariano (1995): Forecast comparison tests

---

作成日: 2025-11-30  
作成者: 時系列予測ベンチマークプロジェクトチーム

