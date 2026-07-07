#!/usr/bin/env python3
"""Preprocess the Dezfouli et al. two-armed bandit behavioural data.

Reads the raw upstream file ``data/raw/choices_diagno.csv.zip`` and produces
two tidy tables under ``data/processed/``:

* ``trials.csv``    -- one row per trial (long format), analysis ready.
* ``subjects.csv``  -- one row per subject (group + clinical scores).

The canonical column mapping follows the authors' own loader
(``rnn_hypercoder/src/expr/data_reader.py::read_BD``):

    reward  = 0 if outcome == 'null' else 1
    action  = 0 if key == 'R1' else 1          # R1 -> right, R2 -> left
    block   = trial                            # the 1..12 sequence id

Run from the repository root::

    python3 scripts/preprocess.py

Data source: Dezfouli et al., "Models that learn how humans learn: The case of
decision-making and its disorders" (PLOS Comput Biol 2019); behavioural data
distributed with the NeurIPS 2019 paper implementation
(github.com/adezfouli/rnn_hypercoder, Apache-2.0).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "choices_diagno.csv.zip"
OUT = ROOT / "data" / "processed"

# diag label in the raw file  ->  short group code used downstream
GROUP_MAP = {
    "Depression": "MDD",   # unipolar major depressive disorder
    "Bipolar": "BD",       # bipolar disorder
    "Healthy": "HC",       # healthy control
}

# expected cohort sizes (paper: 34 / 33 / 34 = 101)
EXPECTED_N = {"MDD": 34, "BD": 33, "HC": 34}


def load_raw() -> pd.DataFrame:
    if not RAW.exists():
        sys.exit(f"Raw file not found: {RAW}\n"
                 "Obtain choices_diagno.csv.zip from "
                 "github.com/adezfouli/rnn_hypercoder (data/BD/).")
    # keep_default_na=False so the literal string 'null' in `outcome` is kept,
    # exactly as the authors' loader does.
    return pd.read_csv(RAW, compression="zip", keep_default_na=False)


def build_trials(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()

    # Canonical derived fields (author mapping).
    df["group"] = df["diag"].map(GROUP_MAP)
    if df["group"].isna().any():
        bad = sorted(df.loc[df["group"].isna(), "diag"].unique())
        sys.exit(f"Unmapped diag labels: {bad}")

    df["reward"] = (df["outcome"] != "null").astype(int)
    df["action"] = (df["key"] == "R2").astype(int)      # R1->0, R2->1

    df = df.rename(columns={
        "ID": "subject_id",
        "trial": "sequence",        # 1..12 : which of the 12 sequences
        "block": "block_half",      # 1 or 2 : first/second experimental half
        "condition": "condition",   # 1..6 : reward-probability condition
        "PressRate.sec": "press_rate_sec",
    })

    # Within-sequence step index (0-based), ordered by acquisition time.
    df = df.sort_values(["subject_id", "sequence", "time"], kind="mergesort")
    df["step"] = df.groupby(["subject_id", "sequence"]).cumcount()

    cols = [
        "subject_id", "group", "sequence", "condition", "block_half", "step",
        "time", "key", "choice", "action", "outcome", "reward", "code",
        "press_rate_sec", "Mania", "Depression",
    ]
    trials = df[cols].reset_index(drop=True)
    trials = trials.rename(columns={"Mania": "mania_score",
                                    "Depression": "depression_score"})
    return trials


def build_subjects(trials: pd.DataFrame) -> pd.DataFrame:
    g = trials.groupby("subject_id")
    subjects = g.agg(
        group=("group", "first"),
        n_sequences=("sequence", "nunique"),
        n_trials=("step", "size"),
        mania_score=("mania_score", "first"),
        depression_score=("depression_score", "first"),
        press_rate_sec=("press_rate_sec", "first"),
        mean_reward=("reward", "mean"),
    ).reset_index()
    return subjects.sort_values(["group", "subject_id"]).reset_index(drop=True)


def validate(trials: pd.DataFrame, subjects: pd.DataFrame) -> None:
    counts = subjects["group"].value_counts().to_dict()
    print("Subjects per group:", counts)
    for grp, n in EXPECTED_N.items():
        got = counts.get(grp, 0)
        flag = "OK" if got == n else "!! MISMATCH"
        print(f"  {grp}: {got} (expected {n}) {flag}")
    assert subjects.shape[0] == 101, f"expected 101 subjects, got {subjects.shape[0]}"

    seqs = trials.groupby("subject_id")["sequence"].nunique()
    assert (seqs == 12).all(), "every subject must have 12 sequences"
    assert set(trials["sequence"].unique()) == set(range(1, 13))
    assert set(trials["action"].unique()) <= {0, 1}
    assert set(trials["reward"].unique()) <= {0, 1}
    print(f"Total trials: {len(trials):,}  |  sequences: "
          f"{trials.groupby(['subject_id','sequence']).ngroups:,}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    raw = load_raw()
    trials = build_trials(raw)
    subjects = build_subjects(trials)
    validate(trials, subjects)

    trials.to_csv(OUT / "trials.csv", index=False)
    subjects.to_csv(OUT / "subjects.csv", index=False)
    print(f"Wrote {OUT/'trials.csv'} and {OUT/'subjects.csv'}")


if __name__ == "__main__":
    main()
