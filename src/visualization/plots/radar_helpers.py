from typing import List

from math import pi
import numpy as np
import matplotlib.pyplot as plt

from src.visualization.constants import DARK, GRAY, LIGHT


def calc_axis_angles(num_variables: int) -> List:
    angles = [(n / float(num_variables) * 2 * pi) for n in range(num_variables)]
    angles += angles[:1]
    return angles


def set_axis_start_n_order(ax: plt.Axes) -> None:
    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)


def draw_ylabels(ax: plt.Axes, num_variables: int) -> None:
    # Draw ylabels
    ax.set_rlabel_position(180 / num_variables)
    y_ticks = list(range(20, 101, 20))
    ax.set_yticks(y_ticks, [str(i) for i in y_ticks], size=10)
    ax.set_ylim(0, 100)


def set_plot_colors(ax: plt.Axes) -> None:
    ax.tick_params(colors=DARK)
    ax.grid(color=GRAY)
    ax.spines['polar'].set_color(DARK)
    ax.set_facecolor(LIGHT)


def align_axis_and_add_labels(ax: plt.Axes, angles: List[float], labels: List[str]) -> None:
    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)

    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], labels, color='black', size=12)


def plot_values(ax: plt.Axes, angles: List[float], values: List[float], color: str, label: str = '') -> plt.Line2D:
    # Plot data
    if label != '':
        radar, = ax.plot(angles, values, linewidth=2, color=color, linestyle='solid', label=label)
    else:
        radar, = ax.plot(angles, values, linewidth=2, color=color, linestyle='solid')
    # Fill area
    ax.fill(angles, values, color=color, alpha=0.25)
    return radar
