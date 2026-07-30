from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "scenario_challenge_matrix.csv"
OUTPUT_PDF = ROOT / "figures" / "scenario_challenge_matrix.pdf"
OUTPUT_PNG = ROOT / "figures" / "scenario_challenge_matrix.png"

METADATA_FIELDS = {"profile", "label", "n_configurations", "n_publications"}
STATE_VALUE = {"-": 0, "?": 1, "I": 2, "R": 3}
STATE_LABEL = {"-": "–", "?": "?", "I": "I", "R": "R"}


def read_matrix() -> tuple[list[str], list[str], list[list[str]]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))

    challenges = [name for name in rows[0] if name not in METADATA_FIELDS]
    scenarios = [
        f'{row["profile"]}  {row["label"]} (n={row["n_configurations"]})'
        for row in rows
    ]
    states = [[row[challenge] for challenge in challenges] for row in rows]
    return scenarios, challenges, states


def render() -> None:
    scenarios, challenges, states = read_matrix()
    values = np.array(
        [[STATE_VALUE[state] for state in row] for row in states],
        dtype=int,
    )

    colors = ListedColormap(["#E9ECEF", "#FFF3CD", "#98C6EA", "#0065BD"])
    figure, axis = plt.subplots(figsize=(9.4, 4.25), constrained_layout=True)
    axis.imshow(values, cmap=colors, vmin=-0.5, vmax=3.5, aspect="equal")

    axis.set_xticks(np.arange(len(challenges)), labels=challenges)
    axis.set_yticks(np.arange(len(scenarios)), labels=scenarios)
    axis.set_xlabel("Challenges")
    axis.set_ylabel("Recurring profiles")
    axis.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

    axis.set_xticks(np.arange(-0.5, len(challenges), 1), minor=True)
    axis.set_yticks(np.arange(-0.5, len(scenarios), 1), minor=True)
    axis.grid(which="minor", color="white", linewidth=1.5)
    axis.tick_params(which="minor", bottom=False, left=False)

    for row_index, row in enumerate(states):
        for column_index, state in enumerate(row):
            text_color = "white" if state == "R" else "#1F2933"
            axis.text(
                column_index,
                row_index,
                STATE_LABEL[state],
                ha="center",
                va="center",
                color=text_color,
                fontsize=9,
                fontweight="bold",
            )

    for spine in axis.spines.values():
        spine.set_visible(False)

    legend = [
        Patch(facecolor="#0065BD", label="R  Reported"),
        Patch(facecolor="#98C6EA", label="I  Inferred"),
        Patch(facecolor="#E9ECEF", edgecolor="#CED4DA", label="–  Trigger absent"),
        Patch(facecolor="#FFF3CD", edgecolor="#E5D59A", label="?  Insufficient"),
    ]
    axis.legend(
        handles=legend,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.17),
        ncol=4,
        frameon=False,
        handlelength=1.2,
        columnspacing=1.5,
    )

    figure.savefig(OUTPUT_PDF, bbox_inches="tight")
    figure.savefig(OUTPUT_PNG, dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    render()
