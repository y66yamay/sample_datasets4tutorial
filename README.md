# Sample datasets for tutorial

> リポジトリ: [`y66yamay/sample_datasets4tutorial`](https://github.com/y66yamay/sample_datasets4tutorial)

計算モデルフィッティング（**計算論的表現型 / computational phenotyping**）と、
**精神疾患傾向・症状・診断**との関係を学ぶための、**モデリング実習・デモ用**の
行動データセット集。各データセットは `datasets/<name>/` 配下に、生データ・前処理
スクリプト・tidy形式の整形データ・ドキュメントをそろえて配置する。

## 収録データセット
| データセット | 課題 | 対象・ラベル | 状態 |
|---|---|---|---|
| [`dezfouli_2019`](datasets/dezfouli_2019/) | 2択バンディット | MDD 34 / BD 33 / HC 34（診断＋躁・抑うつスコア） | ✅ 整備済 |
| [`gagne_2020`](datasets/gagne_2020/) | 随伴性ボラティリティ課題（2択） | exp1: GAD/MDD/対照 87名 ・ exp2: online 147名（多数の症状スコア） | ✅ 整備済 |

> 追加のデータセットは相談のうえ整備します（本リポジトリでは自動追加は行いません）。

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
  gagne_2020/                   # 随伴性ボラティリティ課題（GAD/MDD/対照・online）
    README.md
    data/{raw,processed}/
    scripts/
    docs/
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

## データの再配布（ワークショップ等での配布について）
各データは、帰属（attribution）を明記すれば再配布できるライセンスで公開されている。

| データセット | 根拠ライセンス | 再配布 |
|---|---|---|
| dezfouli_2019 | PLOS論文 CC BY 4.0 / Figshareデータ 既定CC0 / コード Apache-2.0 | 帰属明記で可 |
| gagne_2020 | eLife論文 CC BY 4.0（OSFは"No License"だが論文CC BYが根拠） | 帰属明記で可 |

**クラウド等に再ホストして配布する場合は、各データフォルダ内の
`ATTRIBUTION.md` を必ず一緒に配布すること**（帰属義務を満たすためのコピペ用文面と、
改変内容の記載を含む）:
- [`datasets/dezfouli_2019/data/ATTRIBUTION.md`](datasets/dezfouli_2019/data/ATTRIBUTION.md)
- [`datasets/gagne_2020/data/ATTRIBUTION.md`](datasets/gagne_2020/data/ATTRIBUTION.md)

> 補足: Figshare（dezfouli）の "License" 欄が CC0 か否かは配布前に一度確認を推奨。
> 上記はいずれも帰属を付ければ安全に配布できる（CC BY/Apache-2.0の義務を満たし、CC0でも推奨に合致）。
> 本記載は法的助言ではありません。
