#!/usr/bin/env python3
"""PDF サマリレポートを生成する: docs/report.pdf（Gagne 2020）。

  1 ページ目  概要・コホート・課題設計・符号化・出所
  2 ページ目  exp1 診断群別の記述統計テーブル
  3 ページ目  exp1 症状・行動の図
  4 ページ目  ボラティリティ適応（切替率）の図

実行: dataset ルートで  python3 scripts/make_report.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "IPAGothic"
matplotlib.rcParams["axes.unicode_minus"] = False
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
FIG = ROOT / "docs" / "figures"
OUT = ROOT / "docs" / "report.pdf"

INK, MUTED, ACCENT = "#0b0b0b", "#52514e", "#2a78d6"
PAGE = (8.27, 11.69)


def _text_page(pdf, title, blocks):
    fig = plt.figure(figsize=PAGE)
    fig.patch.set_facecolor("white")
    fig.text(0.08, 0.94, title, fontsize=18, color=INK, weight="bold", va="top")
    fig.add_artist(plt.Line2D([0.08, 0.92], [0.915, 0.915], color=ACCENT, lw=2))
    y = 0.88
    for kind, txt in blocks:
        if kind == "h":
            y -= 0.016
            fig.text(0.08, y, txt, fontsize=13, color=ACCENT, weight="bold", va="top")
            y -= 0.030
        else:
            fig.text(0.08, y, txt, fontsize=10.3, color=MUTED, va="top")
            y -= 0.028 * (txt.count("\n") + 1) + 0.009
    pdf.savefig(fig)
    plt.close(fig)


def _table_page(pdf, desc):
    metrics = [
        ("BDI", "抑うつ BDI"),
        ("STAI_Trait", "特性不安 STAI-T"),
        ("PSWQ", "心配 PSWQ"),
        ("MASQ.AD", "MASQ 快消失"),
        ("p_chose_green", "緑選択率"),
        ("rt_mean_ms", "反応時間(ms)"),
    ]
    groups = ["control", "community", "MDD", "GAD"]
    d = desc.set_index("group")
    header = ["指標"] + [f"{g}\n(n={int(d.loc[g,'n_subjects'])})" for g in groups]
    rows = []
    for key, label in metrics:
        row = [label]
        for g in groups:
            m, sd = d.loc[g, f"{key}_mean"], d.loc[g, f"{key}_sd"]
            fmt = "{:.0f}±{:.0f}" if key == "rt_mean_ms" else (
                "{:.2f}±{:.2f}" if key == "p_chose_green" else "{:.1f}±{:.1f}")
            row.append(fmt.format(m, sd))
        rows.append(row)

    fig = plt.figure(figsize=PAGE)
    fig.patch.set_facecolor("white")
    fig.text(0.08, 0.94, "exp1 診断群別 記述統計", fontsize=18,
             color=INK, weight="bold", va="top")
    fig.add_artist(plt.Line2D([0.08, 0.92], [0.915, 0.915], color=ACCENT, lw=2))
    fig.text(0.08, 0.89, "被験者×課題単位の値を 平均 ± 標準偏差 で集計（患者群 GAD/MDD と対照群）。",
             fontsize=10.3, color=MUTED, va="top")

    ax = fig.add_axes([0.06, 0.52, 0.88, 0.32])
    ax.axis("off")
    tbl = ax.table(cellText=rows, colLabels=header, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9.5)
    tbl.scale(1, 2.1)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#e6e6e2")
        if r == 0:
            cell.set_facecolor(ACCENT); cell.set_text_props(color="white", weight="bold")
        elif r % 2 == 0:
            cell.set_facecolor("#f6f6f4")
        if c == 0:
            cell.set_text_props(weight="bold", color=INK)

    fig.text(0.08, 0.46,
             "補足:\n"
             "・症状スコア（BDI/STAI-T/PSWQ/MASQ）は患者群（GAD/MDD）が対照群より明確に高い。\n"
             "・緑選択率・反応時間などの素の行動指標は群差が小さい。ボラティリティ適応\n"
             "  （volatile と stable の学習の差）を計算モデルで推定して比較するのが本課題の眼目。\n"
             "・記述統計のみで、群間の統計的検定は行っていない。",
             fontsize=9.7, color=MUTED, va="top")
    pdf.savefig(fig)
    plt.close(fig)


def _image_page(pdf, img, title):
    fig = plt.figure(figsize=PAGE)
    fig.patch.set_facecolor("white")
    fig.text(0.08, 0.95, title, fontsize=14, color=INK, weight="bold", va="top")
    ax = fig.add_axes([0.04, 0.1, 0.92, 0.8]); ax.axis("off")
    ax.imshow(mpimg.imread(img))
    pdf.savefig(fig)
    plt.close(fig)


def main():
    desc = pd.read_csv(PROC / "group_descriptives.csv")
    overview = [
        ("h", "概要"),
        ("p", "Gagne, Zika, Dayan, Bishop (2020, eLife) の確率的2択（緑/青）意思決定\n"
              "課題の行動データと症状スコア。stable ブロックと volatile ブロック（頻繁な\n"
              "逆転）で随伴性のボラティリティを操作し、内在化精神病理での学習適応の障害を\n"
              "調べる。二値結果＋変動ブロックなので Volatile Kalman Filter 等の適合に使える。"),
        ("h", "コホート"),
        ("p", "exp1（実験室）: ユニーク87名。診断群 GAD/MDD と対照群 community/control。\n"
              "  症状表は被験者×課題(pain/reward)で170行。患者64（GAD26+MDD38）/\n"
              "  非患者106（community59+control47）。※行動データのみ cb200（pain）が症状表に無い。\n"
              "exp2（オンライン）: ユニーク147名、全員 online。条件 gain/loss。次元的サンプル。"),
        ("h", "課題設計"),
        ("p", "1条件=180試行（volatile 90 + stable 90、3ラン）。選択肢は緑/青の2択で、\n"
              "各選択肢は二値結果と報酬量(mag)を持つ。exp1=pain/reward、exp2=gain/loss。"),
        ("h", "選択・結果の符号化（著者コードで確認）"),
        ("p", "chose_green=1 で緑を選択、0 で青。green_outcome は緑の二値結果。\n"
              "2択の二値結果はブロック内で反相関するため、選択肢の結果は\n"
              "outcome_chosen = green_outcome（緑選択時）/ 1-green_outcome（青選択時）。\n"
              "事象=1 は reward/gain では良、pain/loss では悪（valence依存）。"),
        ("h", "症状スコア"),
        ("p", "BDI, CESD, EPQ.N, MASQ(AA/AD/AS/DS/MS), PSWQ, STAI_Trait(+anx/dep)。\n"
              "exp1のみ CFQ、exp2のみ STAI_State。"),
        ("h", "出所・ライセンス"),
        ("p", "取得元: github.com/crgagne/volatility_paper_elife（data/ のみ収録）。\n"
              "eLife論文は CC-BY 4.0。DOI: 10.7554/eLife.61387。恒久保管: OSF osf.io/8mzuj。\n"
              "利用時は論文とOSFを出典明記のこと（詳細は data/raw/SOURCE.md）。"),
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(OUT) as pdf:
        info = pdf.infodict()
        info["Title"] = "Gagne 2020 volatility task — サマリレポート"
        info["Author"] = "bandit_MDD_BPD_bandit"
        _text_page(pdf, "Gagne 2020 ボラティリティ課題 — サマリ", overview)
        _table_page(pdf, desc)
        _image_page(pdf, FIG / "exp1_group_summary.png", "exp1 診断群別の症状・行動")
        _image_page(pdf, FIG / "volatility_switch.png", "ボラティリティ適応（切替率）")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
