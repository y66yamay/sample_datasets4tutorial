# Data dictionary

## Task
A two-armed bandit (two-choice) task. On each trial the subject picks one of two
options (**R1** / **R2**, i.e. C1 / C2 in the paper) and probabilistically
receives a reward. Each subject completes **12 sequences** (= 6 reward-probability
`condition`s × 2 experimental halves `block_half`). 101 subjects × 12 = **1212
sequences** in total.

Reward contingency (mean reward rate in the raw data): R1 is always the better
arm; `condition` scales how much better (R1 ≈ 0.25 / 0.12 / 0.08 across the
three condition pairs, R2 ≈ 0.05 throughout).

## Groups
| raw `diag` | code | meaning                         | n   |
|------------|------|---------------------------------|-----|
| Depression | MDD  | unipolar major depression       | 34  |
| Bipolar    | BD   | bipolar disorder                | 33  |
| Healthy    | HC   | healthy control                 | 34  |
| **total**  |      |                                 | 101 |

## `data/processed/trials.csv` — one row per trial
| column            | type  | description |
|-------------------|-------|-------------|
| `subject_id`      | str   | subject identifier (e.g. `s_005_`) |
| `group`           | str   | MDD / BD / HC |
| `sequence`        | int   | 1..12, which of the subject's 12 sequences (raw `trial`) |
| `condition`       | int   | 1..6, reward-probability condition |
| `block_half`      | int   | 1 or 2, first/second experimental half (raw `block`) |
| `step`            | int   | 0-based trial index **within** the sequence, ordered by `time` |
| `time`            | float | acquisition timestamp (ms) |
| `key`             | str   | physical key pressed: R1 / R2 |
| `choice`          | str   | recorded arm choice: R1 / R2 |
| `action`          | int   | canonical action: 0 = R1, 1 = R2 (from `key`, author mapping) |
| `outcome`         | str   | O1 / O2 (rewarded outcome types) or `null` (no reward) |
| `reward`          | int   | 0 / 1 (1 iff `outcome != null`) |
| `code`            | int   | joint code: 1=R1/no, 2=R2/no, 3=R1/reward, 4=R2/reward |
| `press_rate_sec`  | float | subject-level mean press rate (s) |
| `mania_score`     | int   | subject-level mania (ALS) score |
| `depression_score`| int   | subject-level depression score |

## `data/processed/subjects.csv` — one row per subject
| column            | type  | description |
|-------------------|-------|-------------|
| `subject_id`      | str   | subject identifier |
| `group`           | str   | MDD / BD / HC |
| `n_sequences`     | int   | number of sequences (12 for all) |
| `n_trials`        | int   | total trials completed |
| `mania_score`     | int   | mania (ALS) score |
| `depression_score`| int   | depression score |
| `press_rate_sec`  | float | mean press rate (s) |
| `mean_reward`     | float | fraction of rewarded trials |

## Notes / caveats
- **`key` vs `choice`.** Both are R1/R2 and disagree on ~49% of trials — the
  physical left/right key is counterbalanced against arm identity across
  blocks. The canonical `action` follows the **authors' loader**, which derives
  the action from `key`. Both raw columns are preserved so you can re-derive an
  arm-based action from `choice` if your analysis needs it.
- **Trials per sequence vary** (min ~2 up to ~130); sequences are not fixed
  length. Use `step` for within-sequence position.
- **No missing subjects.** Group sizes match the paper exactly (34/33/34 = 101);
  `scripts/preprocess.py` asserts this.
- **Train/test split.** The paper uses 8 train / 4 test sequences per subject,
  but the specific split assignment is not encoded in this raw file; construct
  it deterministically downstream if needed.
