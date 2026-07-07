# bandit_MDD_BPD_bandit

計算モデルフィッティング（**計算論的表現型 / computational phenotyping**）と、
**精神疾患傾向・症状・診断**との関係を学ぶための、**モデリング実習・デモ用**の
行動データセット集。各データセットは `datasets/<name>/` 配下に、生データ・前処理
スクリプト・tidy形式の整形データ・ドキュメントをそろえて配置する。

## 収録データセット
| データセット | 課題 | 対象・ラベル | 状態 |
|---|---|---|---|
| [`dezfouli_2019`](datasets/dezfouli_2019/) | 2択バンディット | MDD 34 / BD 33 / HC 34（診断＋躁・抑うつスコア） | ✅ 整備済 |

> 追加のデータセットはこれから検討・整備します（本リポジトリでは自動追加は行いません）。

詳細は各データセットの README と [`datasets/README.md`](datasets/README.md) を参照。

## ディレクトリ構成
```
README.md                       # 本ファイル（リポジトリ全体の説明）
datasets/
  README.md                     # データセット・カタログ
  dezfouli_2019/                # 2択バンディット課題（MDD/BD/HC）
    README.md
    data/{raw,processed}/
    scripts/                    # preprocess / describe / make_report
    docs/                       # data_dictionary, report.pdf, figures
```

## 各データセットの再現手順（共通の考え方）
各データセット配下で、生データ → 前処理 → 記述統計・レポートの順に実行する。
例（dezfouli_2019）:
```bash
pip install pandas matplotlib
cd datasets/dezfouli_2019
python3 scripts/preprocess.py     # 生データ → data/processed/*.csv
python3 scripts/describe.py       # 図 + group_descriptives.csv
python3 scripts/make_report.py    # docs/report.pdf
```

## ライセンス・引用
データセットごとに出所・ライセンスが異なる。各 `datasets/<name>/data/raw/SOURCE.md`
と `docs/` 内のライセンス表記に従い、対応する原論文を引用すること。
