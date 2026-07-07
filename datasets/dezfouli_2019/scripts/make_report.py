#!/usr/bin/env python3
"""PDF サマリレポートを生成する: docs/report.pdf

前処理済みテーブルと生成済み図から、自己完結したレポートを組み立てる:

  1 ページ目  概要・コホート・デモグラフィック・出所
  2 ページ目  グループ別記述統計テーブル
  3 ページ目  グループ別基本統計量の図
  4 ページ目  系列内の学習曲線

preprocess.py と describe.py の実行後に使う::  python3 scripts/make_report.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "IPAGothic"  # 日本語表示
matplotlib.rcParams["axes.unicode_minus"] = False
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
FIG = ROOT / "docs" / "figures"
OUT = ROOT / "docs" / "report.pdf"

INK, MUTED, ACCENT = "#0b0b0b", "#52514e", "#2a78d6"
PAGE = (8.27, 11.69)  # A4 縦, インチ


def _text_page(pdf, title, blocks):
    fig = plt.figure(figsize=PAGE)
    fig.patch.set_facecolor("white")
    fig.text(0.08, 0.94, title, fontsize=19, color=INK, weight="bold", va="top")
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
        ("depression_score", "抑うつスコア"),
        ("mania_score", "躁スコア"),
        ("press_rate_sec", "押下速度 (秒)"),
        ("mean_reward", "報酬率"),
        ("p_better", "良い腕R1選択率"),
        ("n_trials", "総試行数"),
    ]
    groups = ["HC", "MDD", "BD"]
    d = desc.set_index("group")

    header = ["指標"] + [f"{g}（n={int(d.loc[g,'n_subjects'])}）" for g in groups]
    rows = []
    for key, label in metrics:
        row = [label]
        for g in groups:
            m, sd = d.loc[g, f"{key}_mean"], d.loc[g, f"{key}_sd"]
            fmt = "{:.0f} ± {:.0f}" if key == "n_trials" else (
                "{:.3f} ± {:.3f}" if key == "mean_reward" else "{:.2f} ± {:.2f}")
            row.append(fmt.format(m, sd))
        rows.append(row)

    fig = plt.figure(figsize=PAGE)
    fig.patch.set_facecolor("white")
    fig.text(0.08, 0.94, "グループ別 記述統計", fontsize=19,
             color=INK, weight="bold", va="top")
    fig.add_artist(plt.Line2D([0.08, 0.92], [0.915, 0.915], color=ACCENT, lw=2))
    fig.text(0.08, 0.89, "被験者単位の値を 平均 ± 標準偏差 で集計。",
             fontsize=10.5, color=MUTED, va="top")

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
             "補足:\n"
             "・臨床スコアは想定どおりグループを分離: 抑うつは MDD が最高、"
             "躁は BD が最高。\n"
             "・行動指標のグループ差は小さい — 課題の報酬確率が低いため"
             "（R1 ≈ 0.08〜0.25\n"
             "  に対し R2 ≈ 0.05）、良い腕への選好は全群で弱い。\n"
             "・記述統計のみで、群間の統計的検定は行っていない。",
             fontsize=10, color=MUTED, va="top")
    pdf.savefig(fig)
    plt.close(fig)


def _image_page(pdf, img_path, title):
    fig = plt.figure(figsize=PAGE)
    fig.patch.set_facecolor("white")
    fig.text(0.08, 0.95, title, fontsize=15, color=INK, weight="bold", va="top")
    ax = fig.add_axes([0.04, 0.08, 0.92, 0.82])
    ax.axis("off")
    ax.imshow(mpimg.imread(img_path))
    pdf.savefig(fig)
    plt.close(fig)


def main():
    desc = pd.read_csv(PROC / "group_descriptives.csv")

    overview = [
        ("h", "概要"),
        ("p", "Dezfouli et al. (2019) による 2択バンディット課題の行動データ。\n"
              "単極性うつ病 (MDD)・双極性障害 (BD)・健常対照 (HC) を対象とする。\n"
              "本レポートは前処理済みデータのグループ別記述統計をまとめたもの。"),
        ("h", "コホート"),
        ("p", "MDD  34 名   (元ラベル: Depression)\n"
              "BD   33 名   (元ラベル: Bipolar)\n"
              "HC   34 名   (元ラベル: Healthy)\n"
              "合計 101 名 ・ 各被験者 12 系列 ・ 計 1,212 系列 ・ 132,251 試行。"),
        ("h", "課題設計"),
        ("p", "各被験者は 12 系列を実施 = 6 つの報酬確率条件 × 2 つの実験ブロック。\n"
              "腕 R1 が常に良い選択肢（条件により報酬率 ≈ 0.08〜0.25)、R2 ≈ 0.05。"),
        ("h", "デモグラフィック"),
        ("p", "公開ファイルに含まれる被験者単位の変数は、診断ラベル・躁スコア・\n"
              "抑うつスコア・平均押下速度のみ。年齢・性別・IQ・学歴・服薬などの\n"
              "情報は含まれていない。"),
        ("h", "出所・ライセンス"),
        ("p", "取得元: github.com/adezfouli/rnn_hypercoder (data/BD/, Apache-2.0)。\n"
              "正典データは Figshare の記事 8257259 にも公開。\n"
              "利用時は Dezfouli et al. (NeurIPS 2019; PLOS Comput Biol 2019) を引用。"),
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(OUT) as pdf:
        d = pdf.infodict()
        d["Title"] = "Dezfouli MDD/BD/HC バンディットデータ — サマリレポート"
        d["Author"] = "sample_datasets4tutorial"
        _text_page(pdf, "Dezfouli バンディットデータ — サマリ", overview)
        _table_page(pdf, desc)
        _image_page(pdf, FIG / "group_summary.png",
                    "グループ別 基本統計量（被験者単位）")
        _image_page(pdf, FIG / "learning_curve.png",
                    "系列内での学習曲線（グループ別）")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
