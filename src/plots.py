"""Reusable plotting helpers."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")


def save(fig: plt.Figure, name: str, outdir: str | Path = "outputs/figures") -> Path:
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / f"{name}.png"
    fig.savefig(path, bbox_inches="tight", dpi=150)
    return path


def line_series(df: pd.DataFrame, title: str, ylabel: str = "") -> plt.Figure:
    fig, ax = plt.subplots(figsize=(11, 4))
    df.plot(ax=ax)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    return fig


def normalized_overlay(s1: pd.Series, s2: pd.Series, title: str) -> plt.Figure:
    base = pd.concat([s1, s2], axis=1).dropna().iloc[0]
    normed = pd.concat([s1, s2], axis=1).dropna().div(base) * 100
    return line_series(normed, title=title, ylabel="Index (base = 100)")


def rolling_corr(r1: pd.Series, r2: pd.Series, window: int, title: str) -> plt.Figure:
    rc = r1.rolling(window).corr(r2)
    fig, ax = plt.subplots(figsize=(11, 4))
    rc.plot(ax=ax)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_title(f"{title} (rolling {window}w)")
    ax.set_ylabel("correlation")
    return fig


def corr_heatmap(df: pd.DataFrame, title: str = "Feature correlation") -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax)
    ax.set_title(title)
    return fig
