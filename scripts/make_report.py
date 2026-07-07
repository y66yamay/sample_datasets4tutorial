#!/usr/bin/env python3
"""Build a PDF summary report: docs/report.pdf.

Assembles a self-contained report from the processed tables and the generated
figures:

  page 1  overview, provenance, cohort & demographics note
  page 2  group descriptive-statistics table
  page 3  group descriptives figure
  page 4  within-sequence learning curve

Run after preprocess.py and describe.py::  python3 scripts/make_report.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
FIG = ROOT / "docs" / "figures"
OUT = ROOT / "docs" / "report.pdf"

INK, MUTED, ACCENT = "#0b0b0b", "#52514e", "#2a78d6"
PAGE = (8.27, 11.69)  # A4 portrait, inches


def _text_page(pdf, title, blocks):
    fig = plt.figure(figsize=PAGE)
    fig.patch.set_facecolor("white")
    fig.text(0.08, 0.94, title, fontsize=20, color=INK, weight="bold", va="top")
    fig.add_artist(plt.Line2D([0.08, 0.92], [0.915, 0.915], color=ACCENT, lw=2))
    y = 0.88
    for kind, txt in blocks:
        if kind == "h":
            y -= 0.018
            fig.text(0.08, y, txt, fontsize=13, color=ACCENT, weight="bold", va="top")
            y -= 0.032
        else:
            fig.text(0.08, y, txt, fontsize=10.5, color=MUTED, va="top", wrap=True)
            y -= 0.030 * (txt.count("\n") + 1) + 0.010
    pdf.savefig(fig)
    plt.close(fig)


def _table_page(pdf, desc):
    metrics = [
        ("depression_score", "Depression score"),
        ("mania_score", "Mania score"),
        ("press_rate_sec", "Press rate (s)"),
        ("mean_reward", "Reward rate"),
        ("p_better", "P(better arm R1)"),
        ("n_trials", "Trials completed"),
    ]
    groups = ["HC", "MDD", "BD"]
    d = desc.set_index("group")

    header = ["Metric"] + [f"{g} (n={int(d.loc[g,'n_subjects'])})" for g in groups]
    rows = []
    for key, label in metrics:
        row = [label]
        for g in groups:
            m, sd = d.loc[g, f"{key}_mean"], d.loc[g, f"{key}_sd"]
            fmt = "{:.0f} ± {:.0f}" if key == "n_trials" else (
                "{:.3f} ± {:.3f}" if key in ("mean_reward",) else "{:.2f} ± {:.2f}")
            row.append(fmt.format(m, sd))
        rows.append(row)

    fig = plt.figure(figsize=PAGE)
    fig.patch.set_facecolor("white")
    fig.text(0.08, 0.94, "Group descriptive statistics", fontsize=20,
             color=INK, weight="bold", va="top")
    fig.add_artist(plt.Line2D([0.08, 0.92], [0.915, 0.915], color=ACCENT, lw=2))
    fig.text(0.08, 0.89, "Per-subject values summarised as mean ± standard "
             "deviation.", fontsize=10.5, color=MUTED, va="top")

    ax = fig.add_axes([0.08, 0.50, 0.84, 0.34])
    ax.axis("off")
    tbl = ax.table(cellText=rows, colLabels=header, loc="center", cellLoc="left")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.9)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#e6e6e2")
        if r == 0:
            cell.set_facecolor(ACCENT)
            cell.set_text_props(color="white", weight="bold")
        elif r % 2 == 0:
            cell.set_facecolor("#f6f6f4")
        if c == 0:
            cell.set_text_props(weight="bold", color=INK)

    fig.text(0.08, 0.44,
             "Notes:\n"
             "• Clinical scores separate the groups as expected: depression "
             "highest in MDD, mania highest in BD.\n"
             "• Behavioural group differences are small — the task uses low "
             "reward probabilities (R1 ≈ 0.08–0.25\n"
             "   vs R2 ≈ 0.05), so preference for the better arm is weak "
             "across all groups.\n"
             "• Descriptive statistics only; no group-difference tests were "
             "performed.",
             fontsize=10, color=MUTED, va="top")
    pdf.savefig(fig)
    plt.close(fig)


def _image_page(pdf, img_path, title):
    fig = plt.figure(figsize=PAGE)
    fig.patch.set_facecolor("white")
    fig.text(0.08, 0.95, title, fontsize=16, color=INK, weight="bold", va="top")
    ax = fig.add_axes([0.04, 0.08, 0.92, 0.82])
    ax.axis("off")
    ax.imshow(mpimg.imread(img_path))
    pdf.savefig(fig)
    plt.close(fig)


def main():
    desc = pd.read_csv(PROC / "group_descriptives.csv")

    overview = [
        ("h", "Overview"),
        ("p", "Two-armed bandit (two-choice) behavioural data from Dezfouli et\n"
              "al. (2019), covering unipolar depression (MDD), bipolar disorder\n"
              "(BD) and healthy controls (HC). This report summarises the\n"
              "preprocessed dataset with group-level descriptive statistics."),
        ("h", "Cohort"),
        ("p", "MDD  34 subjects   (raw label: Depression)\n"
              "BD   33 subjects   (raw label: Bipolar)\n"
              "HC   34 subjects   (raw label: Healthy)\n"
              "Total 101 subjects · 12 sequences each · 1,212 sequences ·\n"
              "132,251 trials."),
        ("h", "Task design"),
        ("p", "Each subject completes 12 sequences = 6 reward-probability\n"
              "conditions × 2 experimental halves. Arm R1 is always the better\n"
              "option (reward rate ≈ 0.08–0.25 by condition); R2 ≈ 0.05."),
        ("h", "Demographics"),
        ("p", "The only subject-level variables in the released file are the\n"
              "diagnosis label, a mania score, a depression score and a mean\n"
              "press rate. No age, sex, IQ, education or medication data are\n"
              "included."),
        ("h", "Provenance & license"),
        ("p", "Source: github.com/adezfouli/rnn_hypercoder (data/BD/,\n"
              "Apache-2.0); canonical dataset on Figshare article 8257259.\n"
              "Cite Dezfouli et al. (NeurIPS 2019; PLOS Comput Biol 2019)."),
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(OUT) as pdf:
        d = pdf.infodict()
        d["Title"] = "Dezfouli MDD/BD/HC bandit data — summary report"
        d["Author"] = "bandit_MDD_BPD_bandit"
        _text_page(pdf, "Dezfouli bandit data — summary", overview)
        _table_page(pdf, desc)
        _image_page(pdf, FIG / "group_summary.png",
                    "Group descriptives (per subject)")
        _image_page(pdf, FIG / "learning_curve.png",
                    "Learning within a sequence, by group")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
