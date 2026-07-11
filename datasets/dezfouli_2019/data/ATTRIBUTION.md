# ATTRIBUTION — Dezfouli et al. (2019) two-armed bandit data

このフォルダのデータを**再配布・共有する際は、本ファイルを必ず同梱**してください
（例: クラウドに置いて実習参加者にダウンロードさせる場合）。

## データセット
2択バンディット課題の行動データ。単極性うつ病（MDD, n=34）/ 双極性障害（BD, n=33）
/ 健常対照（HC, n=34）。

## 原著者・出典
- Dezfouli, A., Ashtiani, H., Ghattas, O., Nock, R., Dayan, P., & Ong, C. S.
  (2019). *Disentangled behavioural representations.* **NeurIPS 2019.**
- Dezfouli, A., et al. (2019). *Models that learn how humans learn: The case of
  decision-making and its disorders.* **PLOS Computational Biology**, 15(6),
  e1006903. <https://doi.org/10.1371/journal.pcbi.1006903>

- PLOS 論文（オープンアクセス）:
  <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006903>
- データ（PLOS Figshare コレクション / データセット）:
  <https://plos.figshare.com/collections/Models_that_learn_how_humans_learn_The_case_of_decision-making_and_its_disorders/4537250>
  ・ <https://figshare.com/articles/dataset/Models_that_learn_how_humans_learn_The_case_of_decision-making_and_its_disorders/8257259>
- コード・データのGitHub（本データの直接取得元）:
  <https://github.com/adezfouli/rnn_hypercoder>（`data/BD/`）

## ライセンスと再配布可否
このデータには複数の出所が関わり、いずれも**帰属明記のうえで再配布が可能**です。
- **PLOS 論文本体: CC BY 4.0**（<https://creativecommons.org/licenses/by/4.0/>）。
- **Figshare のデータ本体: 既定は CC0（パブリックドメイン）**。PLOS/Figshare のデータは
  通常 CC0 で提供される（CC0 は帰属義務なしだが、学術慣行として帰属を強く推奨）。
  ※ **正確なライセンス表示は Figshare 記事ページ（8257259）の "License" 欄で確認可能**。
- **GitHub コードリポジトリ（rnn_hypercoder）: Apache License 2.0**
  （再配布可・ライセンス表示と帰属が必要。全文は
  [`../docs/UPSTREAM_LICENSE_Apache-2.0.txt`](../docs/UPSTREAM_LICENSE_Apache-2.0.txt)）。

→ CC0 / CC BY / Apache-2.0 のいずれであっても、**下記の帰属表示を付けて配布すれば安全**です
（帰属は CC BY・Apache-2.0 の義務を満たし、CC0 でも推奨に合致）。

### そのまま使える帰属表示（コピペ用）
> Data: Dezfouli, A., et al. (2019). Models that learn how humans learn: The
> case of decision-making and its disorders. PLOS Computational Biology, 15(6),
> e1006903. https://doi.org/10.1371/journal.pcbi.1006903 — and Dezfouli et al.
> (2019), Disentangled behavioural representations, NeurIPS 2019. Data via
> figshare (article 8257259) / https://github.com/adezfouli/rnn_hypercoder.
> Files were reorganized and additional tidy/derived tables were generated for
> teaching purposes (see below).

## 改変（indicate changes）
- `raw/` … 上流 GitHub の `data/BD/choices_diagno.csv.zip` を**内容改変なしでコピー**。
- `processed/` … `raw/` から本リポジトリのスクリプトで生成した**整形・派生データ**。
  生成手順は [`../scripts/preprocess.py`](../scripts/preprocess.py) と
  [`../docs/data_dictionary.md`](../docs/data_dictionary.md) を参照。

## 免責
本ファイルは一般的な帰属情報の整理であり、法的助言ではありません。**Figshare の
"License" 欄（CC0 か否か）を配布前に一度確認**することを推奨します。所属機関で正式に
配布する場合は機関の規程等もご確認ください。データは公開時点で匿名化されています。
