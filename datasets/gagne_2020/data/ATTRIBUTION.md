# ATTRIBUTION — Gagne et al. (2020) volatility task data

このフォルダのデータを**再配布・共有する際は、本ファイルを必ず同梱**してください
（例: クラウドに置いて実習参加者にダウンロードさせる場合）。

## データセット
確率的2択（緑/青）意思決定課題の行動データと症状スコア（stable / volatile ブロック）。

## 原著者・出典
Gagne, C., Zika, O., Dayan, P., & Bishop, S. J. (2020). *Impaired adaptation of
learning to contingency volatility in internalizing psychopathology.* **eLife**,
9, e61387. <https://doi.org/10.7554/eLife.61387>

- 論文（eLife, オープンアクセス全文）: <https://elifesciences.org/articles/61387>
- PMC 版（全文）: <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7755392/>
- データ保管（OSF）: <https://osf.io/8mzuj/>
- コード・データのGitHubミラー（本データの直接取得元）:
  <https://github.com/crgagne/volatility_paper_elife>（`data/` フォルダ）

## ライセンスと再配布可否
- **根拠ライセンス: Creative Commons Attribution 4.0 International（CC BY 4.0）。**
  eLife の全論文および付随データは CC BY 4.0 で公開されており、**出典明記を条件に、
  複製・再配布・改変（商用含む）が許可**されています。
  ライセンス全文: <https://creativecommons.org/licenses/by/4.0/>
- 補足: OSF プロジェクト（8mzuj）側の License 欄は「No License」表示だが、本データは
  上記 CC BY 4.0 の eLife 論文に付随して公開されたものであり、その CC BY 4.0 を根拠と
  する。GitHub ミラーには明示的な LICENSE ファイルは無い。

## 再配布時に満たすべき CC BY 4.0 の条件
1. 原著者名の表示（上記 4 名）
2. 出典（論文タイトル・eLife・DOI）と元リンクの明示
3. ライセンス名（CC BY 4.0）とそのリンクの明示
4. 改変の有無の明示（下記「改変」を参照）
5. 追加の利用制限を課さない

### そのまま使える帰属表示（コピペ用）
> Data: Gagne, C., Zika, O., Dayan, P., & Bishop, S. J. (2020). Impaired
> adaptation of learning to contingency volatility in internalizing
> psychopathology. eLife, 9, e61387. https://doi.org/10.7554/eLife.61387 —
> Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/).
> Retrieved from https://github.com/crgagne/volatility_paper_elife /
> https://osf.io/8mzuj/. Some files were reorganized and additional
> tidy/derived tables were generated for teaching purposes (see below).

## 改変（indicate changes）
- `raw/` … 上流 GitHub リポジトリの `data/` を**内容改変なしでコピー**（macOS由来の
  `.DS_Store` / `Icon` のみ除外）。
- `processed/` … `raw/` から本リポジトリのスクリプトで生成した**整形・派生データ**
  （tidy 化・選択/結果の符号化・被験者要約）。生成手順は
  [`../scripts/preprocess.py`](../scripts/preprocess.py) と
  [`../docs/data_dictionary.md`](../docs/data_dictionary.md) を参照。

## 免責
本ファイルは一般的な帰属情報の整理であり、法的助言ではありません。所属機関で正式に
配布する場合は、機関の規程等もご確認ください。データは公開時点で匿名化されています。
