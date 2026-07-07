#!/usr/bin/env python3
"""Gagne et al. (2020) の基本統計量と図を生成する。

前処理済みテーブルを読み、以下を書き出す:

* ``docs/figures/exp1_group_summary.png`` -- exp1 診断群別の症状・行動（箱+散布）。
* ``docs/figures/volatility_switch.png``  -- stable/volatile ブロック別の切替率
                                             （随伴性ボラティリティ適応の記述指標）。

実行: dataset ルートで  python3 scripts/describe.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "IPAGothic"
matplotlib.rcParams["axes.unicode_minus"] = False
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
FIG = ROOT / "docs" / "figures"

ORDER = ["control", "community", "MDD", "GAD"]          # 対照 → 患者
COLOR = {"control": "#2a78d6", "community": "#1baf7a",
         "MDD": "#eda100", "GAD": "#e34948"}
LABEL = {"control": "control（対照）", "community": "community（地域対照）",
         "MDD": "MDD（うつ）", "GAD": "GAD（不安）"}
BLOCKC = {"stable": "#2a78d6", "volatile": "#e34948"}
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e6e2"


def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.yaxis.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)


def _box_strip(ax, df, col, title, ylabel):
    for i, g in enumerate(ORDER):
        vals = pd.to_numeric(df.loc[df.group == g, col], errors="coerce").dropna().values
        if len(vals) == 0:
            continue
        bp = ax.boxplot(vals, positions=[i], widths=0.55, patch_artist=True,
                        showfliers=False,
                        medianprops=dict(color=INK, lw=1.6),
                        whiskerprops=dict(color=MUTED, lw=1.2),
                        capprops=dict(color=MUTED, lw=1.2), boxprops=dict(lw=0))
        for b in bp["boxes"]:
            b.set(facecolor=COLOR[g], alpha=0.28)
        jit = (np.arange(len(vals)) % 11 - 5) / 5 * 0.13
        ax.scatter(np.full(len(vals), i) + jit, vals, s=13, color=COLOR[g],
                   edgecolor="white", linewidth=0.4, zorder=3, alpha=0.9)
        ax.text(i, ax.get_ylim()[1], f"平均={np.mean(vals):.2f}", ha="center",
                va="bottom", fontsize=8, color=MUTED)
    ax.set_xticks(range(len(ORDER)))
    ax.set_xticklabels(["control", "community", "MDD", "GAD"], fontsize=8.5)
    ax.set_title(title, fontsize=11, color=INK, loc="left", pad=16)
    ax.set_ylabel(ylabel, fontsize=9, color=MUTED)
    _style(ax)


def make_exp1_summary(subjects):
    df = subjects[subjects.exp == "exp1"].copy()
    fig, axes = plt.subplots(2, 3, figsize=(12, 7.4))
    fig.patch.set_facecolor("#fcfcfb")
    panels = [
        ("BDI", "抑うつ BDI", "スコア"),
        ("STAI_Trait", "特性不安 STAI-T", "スコア"),
        ("PSWQ", "心配 PSWQ", "スコア"),
        ("p_chose_green", "緑を選ぶ確率", "割合"),
        ("p_outcome_chosen", "選択肢の事象生起率※", "割合"),
        ("rt_mean_ms", "平均反応時間", "ms"),
    ]
    for ax, (c, t, yl) in zip(axes.ravel(), panels):
        _box_strip(ax, df, c, t, yl)
    handles = [plt.Line2D([0], [0], marker="o", color="w", label=LABEL[g],
                          markerfacecolor=COLOR[g], markersize=9) for g in ORDER]
    fig.suptitle("Gagne 2020 exp1 — 診断群別の症状・行動（被験者×課題単位）",
                 x=0.02, ha="left", fontsize=13, color=INK, y=0.985)
    fig.legend(handles=handles, loc="upper center", ncol=4, frameon=False,
               fontsize=9, bbox_to_anchor=(0.5, 0.95))
    fig.text(0.02, 0.005, "※ 事象生起率=選択肢の二値結果=1の割合。reward/gain では良、pain/loss では悪を意味する（valence依存）。",
             fontsize=8, color=MUTED)
    fig.tight_layout(rect=[0, 0.02, 1, 0.9])
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / "exp1_group_summary.png", dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def switch_rates(trials):
    """被験者×課題×ブロックごとの切替率（前試行と選択が異なる割合）。"""
    d = trials.dropna(subset=["chose_green"]).copy()
    d = d.sort_values(["exp", "subject_id", "task", "run", "trial"])
    grp = ["exp", "subject_id", "task", "run", "block"]
    d["prev"] = d.groupby(grp)["chose_green"].shift(1)
    d["switch"] = (d["chose_green"] != d["prev"]).astype(float)
    d.loc[d["prev"].isna(), "switch"] = np.nan
    sr = d.groupby(["exp", "subject_id", "task", "block"])["switch"].mean().reset_index()
    return sr


def make_volatility_fig(trials, subjects):
    sr = switch_rates(trials)
    sr1 = sr[sr.exp == "exp1"].merge(
        subjects[subjects.exp == "exp1"][["subject_id", "task", "group"]],
        on=["subject_id", "task"], how="left")
    fig, ax = plt.subplots(figsize=(9, 5.2))
    fig.patch.set_facecolor("#fcfcfb")
    width = 0.36
    for j, block in enumerate(["stable", "volatile"]):
        means, cis = [], []
        for g in ORDER:
            v = sr1[(sr1.group == g) & (sr1.block == block)]["switch"].dropna()
            means.append(v.mean())
            cis.append(1.96 * v.std() / np.sqrt(len(v)) if len(v) else 0)
        x = np.arange(len(ORDER)) + (j - 0.5) * width
        ax.bar(x, means, width, yerr=cis, capsize=3, color=BLOCKC[block],
               alpha=0.85, label="stable（安定）" if block == "stable" else "volatile（変動）",
               edgecolor="white", linewidth=1)
    ax.set_xticks(range(len(ORDER)))
    ax.set_xticklabels(["control", "community", "MDD", "GAD"])
    ax.set_ylabel("切替率（前試行と選択が異なる割合）", fontsize=10, color=MUTED)
    ax.set_title("随伴性ボラティリティ適応: stable vs volatile の切替率（exp1・平均±95%CI）",
                 fontsize=12, color=INK, loc="left", pad=10)
    ax.legend(frameon=False, fontsize=9.5)
    _style(ax)
    fig.tight_layout()
    fig.savefig(FIG / "volatility_switch.png", dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    trials = pd.read_csv(PROC / "trials.csv")
    subjects = pd.read_csv(PROC / "subjects.csv")
    make_exp1_summary(subjects)
    make_volatility_fig(trials, subjects)
    print(f"Wrote figures to {FIG}/")


if __name__ == "__main__":
    main()
