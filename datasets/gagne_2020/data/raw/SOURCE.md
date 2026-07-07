# 生データの出所（Gagne et al. 2020）

## 取得元
- リポジトリ: <https://github.com/crgagne/volatility_paper_elife>（`data/` フォルダ）
- 取得日: 2026-07-07、`git clone` 経由（この環境で到達可能だった唯一のホスト）。
- 恒久保管（OSF）: <https://osf.io/8mzuj/>（大きいモデルフィット結果はOSFのみ。本収録では不要のため除外）

## 収録物
上流 `data/` を改変せずコピー（macOS由来の `.DS_Store` / `Icon` は除外）:
```
participant_table_exp1.csv           # exp1 被験者×課題の症状スコア＋群情報
participant_table_exp2.csv           # exp2 同上（オンライン）
participant_table_confirmatory.csv   # 確認的因子分析サンプル
data_raw_exp1/                       # exp1 行動データ（被験者×条件ごとに1 CSV, 171ファイル）
data_raw_exp2/                       # exp2 行動データ（同上, 294ファイル）
item_level_data_for_bifactor_analysis/  # bifactor分析用の項目レベル回答
```

## 論文・DOI
Christopher Gagne, Ondrej Zika, Peter Dayan, Sonia J. Bishop (2020)
"Impaired adaptation of learning to contingency volatility in internalizing
psychopathology." *eLife* 9:e61387.
DOI: <https://doi.org/10.7554/eLife.61387>

## ライセンス・出典
eLife 論文は **CC-BY 4.0**。ただし上流リポジトリに明示的な LICENSE ファイルは
無い。再配布時は必ず**論文と OSF を出典として明記**すること。利用時は上記論文を
引用する。
