"""Render a provenance-labeled heatmap from the pinned PIDS-Bench author table."""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


COMMIT = "87dc835566b930ee921240874a4939b2c266c2fe"
MODELS = ("TF-IDF + LR", "DistilBERT", "DeBERTa-v3-FT")
VALUE_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)(?:\s*±\s*(\d+(?:\.\d+)?))?\s*$")


def pinned_readme(upstream: Path) -> tuple[list[str], str]:
    actual = subprocess.check_output(
        ["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != COMMIT:
        raise SystemExit(f"Expected pinned commit {COMMIT}, found {actual}")
    content = subprocess.check_output(
        ["git", "-C", str(upstream), "show", f"{COMMIT}:README.md"]
    ).decode("utf-8")
    return content.splitlines(), actual


def extract_table(lines: list[str]) -> tuple[list[str], dict[str, list[tuple[float, float | None]]]]:
    header_index = next(
        (i for i, line in enumerate(lines) if "| Model | IID F1" in line), None
    )
    if header_index is None:
        raise SystemExit("Could not find the pinned README internal-baseline table")
    header = [cell.strip() for cell in lines[header_index].strip().strip("|").split("|")]
    rows: dict[str, list[tuple[float, float | None]]] = {}
    for line in lines[header_index + 2 :]:
        if not line.strip().startswith("|"):
            if set(rows) == set(MODELS):
                break
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0] not in MODELS:
            continue
        if len(cells) != len(header):
            raise SystemExit(f"Unexpected author table width for {cells[0]}: {cells}")
        values: list[tuple[float, float | None]] = []
        for cell in cells[1:]:
            match = VALUE_RE.fullmatch(cell)
            if match is None:
                raise SystemExit(f"Could not parse author table value {cell!r}")
            values.append(
                (float(match.group(1)), float(match.group(2)) if match.group(2) else None)
            )
        rows[cells[0]] = values
    if set(rows) != set(MODELS) or len(header) != 9:
        raise SystemExit(f"Incomplete or unexpected author table: {header}; {sorted(rows)}")
    return header[1:], rows


def direction(label: str) -> int:
    return -1 if "↓" in label else 1


def main() -> None:
    report_dir = Path(__file__).resolve().parent
    member_root = report_dir.parents[2]
    upstream = member_root / "replications" / "PIDS_Bench_Shire_IEEEAccess2026" / "upstream"
    lines, source_commit = pinned_readme(upstream)
    headers, rows = extract_table(lines)

    csv_path = report_dir / "pids_bench_author_published_matrix.csv"
    parsed: list[dict[str, object]] = []
    for model in MODELS:
        for label, (mean, std) in zip(headers, rows[model], strict=True):
            parsed.append(
                {
                    "model": model,
                    "metric": label,
                    "mean": mean,
                    "std": "" if std is None else std,
                    "direction": "lower_is_better" if direction(label) < 0 else "higher_is_better",
                    "provenance": "author-published; not a local transformer run",
                    "source_commit": source_commit,
                    "source_file": "README.md",
                }
            )
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(parsed[0]))
        writer.writeheader()
        writer.writerows(parsed)

    means = np.array([[value[0] for value in rows[model]] for model in MODELS])
    normalized = np.zeros_like(means)
    for column, label in enumerate(headers):
        values = means[:, column] * direction(label)
        low, high = values.min(), values.max()
        normalized[:, column] = 0.5 if high == low else (values - low) / (high - low)

    fig, ax = plt.subplots(figsize=(19, 5.8))
    image = ax.imshow(normalized, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(np.arange(len(headers)), labels=headers, fontsize=9)
    ax.set_yticks(np.arange(len(MODELS)), labels=MODELS, fontsize=10)
    ax.tick_params(axis="x", top=True, bottom=False, labeltop=True, labelbottom=False, length=0, pad=9)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.set_xticklabels(headers, rotation=0, ha="center")
    ax.set_xticks(np.arange(-0.5, len(headers), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(MODELS), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)
    for row_index, model in enumerate(MODELS):
        for column, (_, (mean, std)) in enumerate(zip(headers, rows[model], strict=True)):
            label = f"{mean * 100:.2f}%" if std is None else f"{mean * 100:.2f} ± {std * 100:.2f}%"
            cell_color = "white" if normalized[row_index, column] < 0.22 or normalized[row_index, column] > 0.84 else "#15213a"
            ax.text(column, row_index, label, ha="center", va="center", fontsize=8.3, color=cell_color, weight="semibold")
    fig.suptitle("PIDS-Bench · Author-Published Internal Baselines", fontsize=17, weight="bold", y=0.96)
    fig.subplots_adjust(left=0.09, right=0.96, top=0.80, bottom=0.27)
    fig.text(
        0.5,
        0.15,
        "Fixed τ=0.5 · Transformer results are 5-seed means ± SD; TF-IDF is deterministic. "
        "Color ranks models within each metric; cell labels are the author-reported values. Hard-benign n=1,472.",
        ha="center",
        va="center",
        fontsize=9,
        color="#334155",
    )
    fig.text(
        0.5,
        0.085,
        "Local TF-IDF was reproduced; DeBERTa seed 42 paused at 4,281/5,082 with checkpoint-3388 (epoch 2) as the latest durable state; DistilBERT has not started. No local transformer test score or cascade result is available.",
        ha="center",
        va="center",
        fontsize=9,
        color="#334155",
    )
    fig.colorbar(image, ax=ax, fraction=0.015, pad=0.012, label="Relative rank within metric (green = better)")
    figure_path = report_dir / "pids_bench_author_published_matrix.png"
    fig.savefig(figure_path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"source_commit={source_commit}")
    print(f"csv={csv_path}")
    print(f"figure={figure_path}")


if __name__ == "__main__":
    main()
