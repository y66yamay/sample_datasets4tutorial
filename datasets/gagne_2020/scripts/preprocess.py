#!/usr/bin/env python3
"""Preprocess the Gagne et al. (2020, eLife) volatility task data.

Reads the raw upstream files under ``data/raw/`` and produces tidy tables under
``data/processed/``:

* ``trials.csv``    -- one row per trial (both experiments, long format).
* ``subjects.csv``  -- one row per subject × task file (symptom scores, group,
                       and per-file behavioural summaries).
* ``group_descriptives.csv`` -- exp1 group-level summary (diagnostic groups).

Choice / outcome coding (verified against the authors'
``data_processing_code/get_data.py``):

    chose_green    = choice            # 1 = chose green, 0 = chose blue
    green_outcome  = binary outcome of the GREEN option (0/1)
    # the two options' binary outcomes are anti-correlated within a block, so
    # the outcome of the CHOSEN option is:
    outcome_chosen = green_outcome     if chose_green else 1 - green_outcome

Run from the dataset root::  python3 scripts/preprocess.py

Data: Gagne, Zika, Dayan, Bishop (2020) eLife 9:e61387 (CC-BY 4.0).
Source: github.com/crgagne/volatility_paper_elife . See data/raw/SOURCE.md.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"

# condition token (in the behaviour filename) -> participant_table `task` value
COND_TO_TASK = {"rew": "reward", "pain": "pain", "gain": "gain", "loss": "loss"}

# symptom score columns (union across experiments; missing ones become NA)
SYMPTOMS = [
    "BDI", "CESD", "EPQ.N", "MASQ.AA", "MASQ.AD", "MASQ.AS", "MASQ.DS",
    "MASQ.MS", "PSWQ", "STAI_Trait", "STAI_Trait_anx", "STAI_Trait_dep",
    "CFQ", "STAI_State",  # exp1-only / exp2-only respectively
]
GROUP_COLS = ["group", "group_p_c", "group_just_patients"]

EXP1_RE = re.compile(r"behavioral_trial_table_(?P<mid>.+)_(?P<cond>rew|pain)_modelready\.csv")
EXP2_RE = re.compile(r"behavioral_tablehit_batch_(?P<cond>gain|loss)_(?P<mid>.+)_modelready\.csv")


def _read_trials(path: Path, exp: str, mid: str, cond: str) -> pd.DataFrame:
    d = pd.read_csv(path, index_col=0)
    d = d.reset_index(drop=True)
    d.insert(0, "exp", exp)
    d.insert(1, "subject_id", mid)
    d.insert(2, "cond", cond)
    d.insert(3, "task", COND_TO_TASK[cond])
    d.insert(4, "trial", range(len(d)))          # 0-based within file
    gc = d["choice"].astype("Int64")             # 1 = green, 0 = blue, <NA> = no response
    go = d["green_outcome"].astype("Int64")
    d["chose_green"] = gc
    # outcome of the chosen option (see module docstring); NA-safe, vectorised
    oc = pd.Series(pd.NA, index=d.index, dtype="Int64")
    oc[gc == 1] = go[gc == 1]
    oc[gc == 0] = (1 - go)[gc == 0]
    d["outcome_chosen"] = oc
    cm = d["green_mag"].where(gc == 1, d["blue_mag"])
    d["chosen_mag"] = cm.where(gc.notna())
    return d


def collect_trials() -> pd.DataFrame:
    rows = []
    for f in sorted((RAW / "data_raw_exp1").glob("*.csv")):
        m = EXP1_RE.match(f.name)
        if m:
            rows.append(_read_trials(f, "exp1", m["mid"], m["cond"]))
    for f in sorted((RAW / "data_raw_exp2").glob("*.csv")):
        m = EXP2_RE.match(f.name)
        if m:
            rows.append(_read_trials(f, "exp2", m["mid"], m["cond"]))
    cols = ["exp", "subject_id", "cond", "task", "run", "block", "trial",
            "chose_green", "green_outcome", "outcome_chosen",
            "green_mag", "blue_mag", "chosen_mag", "rt"]
    return pd.concat(rows, ignore_index=True)[cols]


def load_participants() -> pd.DataFrame:
    frames = []
    for exp, fn in [("exp1", "participant_table_exp1.csv"),
                    ("exp2", "participant_table_exp2.csv")]:
        pt = pd.read_csv(RAW / fn, index_col=0)
        pt["exp"] = exp
        keep = ["exp", "MID", "task"] + GROUP_COLS + \
               [c for c in SYMPTOMS if c in pt.columns]
        pt = pt[[c for c in keep if c in pt.columns]].copy()
        for c in SYMPTOMS:                       # ensure a uniform column set
            if c not in pt.columns:
                pt[c] = pd.NA
        frames.append(pt)
    p = pd.concat(frames, ignore_index=True)
    return p.rename(columns={"MID": "subject_id"})


def behavioural_summary(trials: pd.DataFrame) -> pd.DataFrame:
    g = trials.groupby(["exp", "subject_id", "task"])
    summ = g.agg(
        n_trials=("trial", "size"),
        n_volatile=("block", lambda b: int((b == "volatile").sum())),
        n_stable=("block", lambda b: int((b == "stable").sum())),
        p_chose_green=("chose_green", "mean"),
        # event rate of the chosen option (valence-neutral: 1 = the binary event
        # occurred; that is GOOD for reward/gain but BAD for pain/loss)
        p_outcome_chosen=("outcome_chosen", "mean"),
        rt_mean_ms=("rt", "mean"),
    ).reset_index()
    return summ


def build_subjects(trials: pd.DataFrame, parts: pd.DataFrame) -> pd.DataFrame:
    summ = behavioural_summary(trials)
    # exp1 joins on (subject_id, task); exp2 participant table has one row per
    # subject (task == 'reward'), so join exp2 on subject_id only.
    p1 = parts[parts.exp == "exp1"]
    p2 = parts[parts.exp == "exp2"].drop(columns=["task"])
    s1 = summ[summ.exp == "exp1"].merge(p1, on=["exp", "subject_id", "task"], how="left")
    s2 = summ[summ.exp == "exp2"].merge(p2, on=["exp", "subject_id"], how="left")
    subjects = pd.concat([s1, s2], ignore_index=True)
    front = ["exp", "subject_id", "task"] + GROUP_COLS + \
            ["n_trials", "n_volatile", "n_stable",
             "p_chose_green", "p_outcome_chosen", "rt_mean_ms"] + SYMPTOMS
    return subjects[[c for c in front if c in subjects.columns]]


def group_descriptives(subjects: pd.DataFrame) -> pd.DataFrame:
    s = subjects[subjects.exp == "exp1"].copy()
    metrics = ["p_outcome_chosen", "p_chose_green", "rt_mean_ms",
               "BDI", "STAI_Trait", "PSWQ", "MASQ.AD"]
    rows = []
    for grp, sub in s.groupby("group"):
        row = {"group": grp, "n_rows": len(sub),
               "n_subjects": sub["subject_id"].nunique()}
        for m in metrics:
            row[f"{m}_mean"] = round(pd.to_numeric(sub[m], errors="coerce").mean(), 3)
            row[f"{m}_sd"] = round(pd.to_numeric(sub[m], errors="coerce").std(), 3)
        rows.append(row)
    return pd.DataFrame(rows)


def validate(trials, subjects):
    n1 = trials[trials.exp == "exp1"]["subject_id"].nunique()
    n2 = trials[trials.exp == "exp2"]["subject_id"].nunique()
    print(f"exp1 subjects: {n1}  |  exp2 subjects: {n2}")
    print("exp1 groups (subject×task rows):",
          subjects[subjects.exp == "exp1"]["group"].value_counts().to_dict())
    tpf = trials.groupby(["exp", "subject_id", "task"]).size()
    print(f"trials per file: min {tpf.min()} / median {int(tpf.median())} / max {tpf.max()}")
    assert set(trials["block"].dropna().unique()) == {"volatile", "stable"}
    assert set(trials["chose_green"].dropna().unique()) <= {0, 1}
    assert set(trials["outcome_chosen"].dropna().unique()) <= {0, 1}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    trials = collect_trials()
    parts = load_participants()
    subjects = build_subjects(trials, parts)
    validate(trials, subjects)

    trials.to_csv(OUT / "trials.csv", index=False)
    subjects.to_csv(OUT / "subjects.csv", index=False)
    group_descriptives(subjects).to_csv(OUT / "group_descriptives.csv", index=False)
    print(f"trials: {len(trials):,} rows  |  subjects: {len(subjects)} rows")
    print(f"Wrote {OUT}/trials.csv, subjects.csv, group_descriptives.csv")


if __name__ == "__main__":
    main()
