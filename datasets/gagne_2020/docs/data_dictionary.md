# データディクショナリ（Gagne et al. 2020）

## 課題
確率的2択（**緑 / 青**）意思決定課題。各試行で緑か青を選び、選択肢は二値結果
（0/1）と報酬量（`mag`）を持つ。**stable ブロック**（随伴性が安定）と
**volatile ブロック**（頻繁に逆転）で随伴性のボラティリティを操作する。
1条件 = **180試行**（volatile 90 + stable 90、3ラン）。

- exp1（実験室）: 課題条件 = `pain`（電気刺激）/ `reward`（報酬）
- exp2（オンライン）: 課題条件 = `gain`（獲得）/ `loss`（損失）

## 群・サンプル
| 実験 | ユニーク被験者 | 群 |
|---|---|---|
| exp1 | 87 | GAD 26 / MDD 38（患者64）・community 59 / control 47（非患者106）※行数=被験者×課題で170 |
| exp2 | 147 | 全員 online（次元的サンプル、症状は連続スコア） |

> ※ 行動データのみ `cb200`（pain）が症状表に存在せず、`subjects.csv` では群・症状が NA。

## `data/processed/trials.csv` — 1行 = 1試行
| カラム | 型 | 説明 |
|---|---|---|
| `exp` | str | `exp1` / `exp2` |
| `subject_id` | str | 被験者ID（`MID`。exp1例 `cb25`, exp2例 `mturk0`） |
| `cond` | str | 生の条件トークン（`rew`/`pain`/`gain`/`loss`） |
| `task` | str | 正規化した課題名（`reward`/`pain`/`gain`/`loss`） |
| `run` | float | ラン番号（0〜2） |
| `block` | str | `volatile` / `stable` |
| `trial` | int | ファイル内の試行インデックス（0始まり） |
| `chose_green` | Int64 | 1=緑を選択, 0=青, `<NA>`=無反応 |
| `green_outcome` | int | 緑オプションの二値結果（0/1） |
| `outcome_chosen` | Int64 | 選択した側の二値結果（下記の符号化参照） |
| `green_mag` | float | 緑の報酬量（pain/loss では負値あり） |
| `blue_mag` | float | 青の報酬量 |
| `chosen_mag` | float | 選択した側の報酬量 |
| `rt` | float | 反応時間（ミリ秒とみられる） |

## `data/processed/subjects.csv` — 1行 = 被験者×課題
| カラム | 説明 |
|---|---|
| `exp`, `subject_id`, `task` | 主キー |
| `group` | exp1: GAD/MDD/community/control ・ exp2: online |
| `group_p_c` | patient / nonpatient |
| `group_just_patients` | 患者の診断名（患者行のみ） |
| `n_trials`, `n_volatile`, `n_stable` | 試行数 |
| `p_chose_green` | 緑選択率 |
| `p_outcome_chosen` | 選択肢の事象生起率（**valence依存**: reward/gainで良, pain/lossで悪） |
| `rt_mean_ms` | 平均反応時間 |
| 症状スコア | BDI, CESD, EPQ.N, MASQ.AA/AD/AS/DS/MS, PSWQ, STAI_Trait(+anx/dep), CFQ(exp1), STAI_State(exp2) |

## 選択・結果の符号化（重要）
著者の `data_processing_code/get_data.py` で確認済み:

```
chose_green    = choice            # 1 = 緑, 0 = 青
green_outcome  = 緑オプションの二値結果（0/1）
# 2択の二値結果はブロック内で反相関するため:
outcome_chosen = green_outcome        （緑を選択した試行）
               = 1 - green_outcome    （青を選択した試行）
```

`outcome_chosen = 1` は「選択肢の事象が生起」を意味し、**reward/gain では良い事象、
pain/loss では悪い事象**（valence依存）。VKF 等のフィッティングでは `chose_green` と
`outcome_chosen` を入力にすると符号の取り違えを避けられる。

## 注意点
- **無反応試行**: `chose_green` が `<NA>` の試行が約0.45%（380/83,700）。`outcome_chosen`
  と `chosen_mag` も NA。
- **`rt` の単位**: 整数でミリ秒とみられるが元データに単位注記なし。
- **ボラティリティ適応**: volatile と stable の学習（例: 推定学習率や切替率）の差が
  本課題の眼目。素の行動指標の群差は小さいので、計算モデルで表現型を推定して比較する。
