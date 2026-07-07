#!/usr/bin/env python3
"""Group-level descriptive statistics and figures for the bandit dataset.

Reads the processed tables and writes:

* ``docs/figures/group_summary.png``   -- clinical & behavioural distributions
                                           by group (box + jitter, 2x3 panels).
* ``docs/figures/learning_curve.png``  -- P(choose better arm) vs within-sequence
                                           step, by group, with 95% CI.
* ``data/processed/group_descriptives.csv`` -- mean/sd/median summary table.

Run from the repo root::  python3 scripts/describe.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "IPAGothic"  # 日本語表示
matplotlib.rcParams["axes.unicode_minus"] = False
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
FIG = ROOT / "docs" / "figures"

# fixed group order (control first) and per-entity colours (colourblind-safe,
# validated categorical slots; colour follows the group, never its rank).
ORDER = ["HC", "MDD", "BD"]
COLOR = {"HC": "#2a78d6", "MDD": "#eda100", "BD": "#1baf7a"}
LABEL = {"HC": "HC（健常）", "MDD": "MDD（単極性うつ）", "BD": "BD（双極性）"}

INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e6e2"


def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.yaxis.grid(True, color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)


def _box_strip(ax, subj, col, title, ylabel):
    for i, g in enumerate(ORDER):
        vals = subj.loc[subj.group == g, col].dropna().values
        bp = ax.boxplot(vals, positions=[i], widths=0.5, patch_artist=True,
                        showfliers=False, zorder=2,
                        medianprops=dict(color=INK, lw=1.6),
                        whiskerprops=dict(color=MUTED, lw=1.2),
                        capprops=dict(color=MUTED, lw=1.2),
                        boxprops=dict(lw=0))
        for b in bp["boxes"]:
            b.set(facecolor=COLOR[g], alpha=0.28)
        # jittered points (deterministic jitter, no RNG)
        jit = (np.arange(len(vals)) % 11 - 5) / 5 * 0.14
        ax.scatter(np.full(len(vals), i) + jit, vals, s=16, color=COLOR[g],
                   edgecolor="white", linewidth=0.5, zorder=3, alpha=0.9)
        ax.text(i, ax.get_ylim()[1], f"平均={np.mean(vals):.2f}", ha="center",
                va="bottom", fontsize=8, color=MUTED)
    ax.set_xticks(range(len(ORDER)))
    ax.set_xticklabels(ORDER)
    ax.set_title(title, fontsize=11, color=INK, loc="left", pad=16)
    ax.set_ylabel(ylabel, fontsize=9, color=MUTED)
    _style(ax)


def make_summary(trials, subj):
    # per-subject behavioural summaries
    beh = trials.groupby("subject_id").agg(
        p_better=("action", lambda a: float((a == 0).mean())),  # R1=action0 is better
    ).reset_index()
    subj = subj.merge(beh, on="subject_id")

    fig, axes = plt.subplots(2, 3, figsize=(12, 7.4))
    fig.patch.set_facecolor("#fcfcfb")
    panels = [
        ("depression_score", "抑うつスコア", "スコア"),
        ("mania_score", "躁スコア", "スコア"),
        ("press_rate_sec", "押下速度", "秒"),
        ("mean_reward", "報酬率（正答率の代理）", "報酬確率"),
        ("p_better", "良い腕R1を選ぶ確率", "割合"),
        ("n_trials", "総試行数", "回"),
    ]
    for ax, (col, title, yl) in zip(axes.ravel(), panels):
        _box_strip(ax, subj, col, title, yl)

    handles = [plt.Line2D([0], [0], marker="o", color="w", label=LABEL[g],
                          markerfacecolor=COLOR[g], markersize=9) for g in ORDER]
    fig.suptitle("Dezfouli バンディットデータ — グループ別基本統計量（被験者単位）",
                 x=0.02, ha="left", fontsize=13, color=INK, y=0.985)
    fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False,
               fontsize=9.5, bbox_to_anchor=(0.5, 0.945))
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / "group_summary.png", dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    return subj


def make_learning_curve(trials):
    MAXSTEP = 40
    d = trials[trials.step < MAXSTEP].copy()
    d["better"] = (d["action"] == 0).astype(float)
    fig, ax = plt.subplots(figsize=(8.4, 5))
    fig.patch.set_facecolor("#fcfcfb")
    for g in ORDER:
        gd = d[d.group == g]
        m = gd.groupby("step")["better"].mean()
        n = gd.groupby("step")["better"].count()
        sd = gd.groupby("step")["better"].std()
        ci = 1.96 * sd / np.sqrt(n)
        ax.fill_between(m.index, m - ci, m + ci, color=COLOR[g], alpha=0.15, lw=0)
        ax.plot(m.index, m.values, color=COLOR[g], lw=2, zorder=3)
        ax.text(m.index[-1] + 0.4, m.values[-1], g, color=COLOR[g],
                fontsize=10, va="center", fontweight="bold")
    ax.axhline(0.5, color=MUTED, lw=1, ls="--", zorder=1)
    ax.set_xlabel("系列内の試行番号（ステップ）", fontsize=10, color=MUTED)
    ax.set_ylabel("良い腕R1を選ぶ確率", fontsize=10, color=MUTED)
    ax.set_title("系列内での学習曲線（グループ別、平均 ± 95% 信頼区間）",
                 fontsize=12, color=INK, loc="left", pad=10)
    ax.set_xlim(-0.5, MAXSTEP + 2)
    _style(ax)
    fig.tight_layout()
    fig.savefig(FIG / "learning_curve.png", dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def make_table(subj):
    metrics = ["depression_score", "mania_score", "press_rate_sec",
               "mean_reward", "p_better", "n_trials"]
    rows = []
    for g in ORDER:
        s = subj[subj.group == g]
        row = {"group": g, "n_subjects": len(s)}
        for m in metrics:
            row[f"{m}_mean"] = round(s[m].mean(), 3)
            row[f"{m}_sd"] = round(s[m].std(), 3)
            row[f"{m}_median"] = round(s[m].median(), 3)
        rows.append(row)
    tab = pd.DataFrame(rows)
    tab.to_csv(PROC / "group_descriptives.csv", index=False)
    with pd.option_context("display.width", 200, "display.max_columns", 50):
        print(tab.to_string(index=False))
    return tab


def main():
    trials = pd.read_csv(PROC / "trials.csv")
    subj = pd.read_csv(PROC / "subjects.csv")
    subj = make_summary(trials, subj)
    make_learning_curve(trials)
    make_table(subj)
    print(f"\nWrote figures to {FIG}/ and group_descriptives.csv")


if __name__ == "__main__":
    main()
