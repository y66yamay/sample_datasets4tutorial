# 生データの出所

## ファイル
- `choices_diagno.csv.zip` — NeurIPS 2019 論文の実装に同梱されている行動データ
  ファイルをそのままコピーしたもの。

## 取得元
- リポジトリ: <https://github.com/adezfouli/rnn_hypercoder>（パス: `data/BD/`）
- 取得日: 2026-07-07、`git clone` 経由（この環境で到達可能だった唯一のホスト）。

## 正典・元データの所在
同じ行動データは Figshare にもデータセットとして公開されている（取得時点では
この環境のネットワークポリシーにより到達不可。参考として記録）:

- PLOS Figshare コレクション:
  <https://plos.figshare.com/collections/Models_that_learn_how_humans_learn_The_case_of_decision-making_and_its_disorders/4537250>
- Figshare データセット:
  <https://figshare.com/articles/dataset/Models_that_learn_how_humans_learn_The_case_of_decision-making_and_its_disorders/8257259>

## 関連論文
- Dezfouli, Ashtiani, Ghattas, Nock, Dayan, Ong (2019).
  *Disentangled behavioural representations.* NeurIPS 2019.
- Dezfouli et al. (2019). *Models that learn how humans learn: The case of
  decision-making and its disorders.* PLOS Computational Biology.

## ライセンス
`rnn_hypercoder` リポジトリは Apache-2.0 ライセンス
（`docs/UPSTREAM_LICENSE_Apache-2.0.txt` を参照）。データ本体の正典ライセンスは
Figshare のデータセット記録を確認すること（PLOS のデータセットは通常 CC BY）。
利用時は上記の論文を引用すること。
