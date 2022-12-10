from typing import List, Tuple

import matplotlib.pyplot as plt

from src.visualization.constants import LIGHT_BLUE, COMPARATOR_COLORS
from src.visualization.plots.radar_helpers import set_axis_start_n_order, calc_axis_angles, align_axis_and_add_labels, \
    draw_ylabels, set_plot_colors, plot_values

MatplotlibSubplots = Tuple[plt.Figure, plt.Axes]


def plot_plt_radar(values: List[float], labels: List[str], ax=None,
                   color: str = LIGHT_BLUE) -> MatplotlibSubplots or None:
    num_variables = len(labels)
    # the angle of each axis in the plot
    angles = calc_axis_angles(num_variables)

    # Initialise the spider plot
    fig = None
    if ax is None:
        fig, ax = plt.subplots(figsize=(4, 3), subplot_kw={'projection': 'polar'})

    set_axis_start_n_order(ax)
    align_axis_and_add_labels(ax, angles, labels)
    draw_ylabels(ax, num_variables)

    radar = plot_values(ax, angles=angles, values=values, color=color)
    setattr(ax, 'radar_plot', radar)

    set_plot_colors(ax)
    plt.tight_layout()
    if fig is not None:
        return fig, ax


ComparatorLabels = List[str]
ComparatorListValues = List[List[float]]
ComparatorListLegendLabels = List[List[str]]


def plot_plt_radar_comparison(values: ComparatorListValues, labels: ComparatorLabels,
                              legend_labels_list: ComparatorListLegendLabels,
                              color_order_list=COMPARATOR_COLORS) -> MatplotlibSubplots or None:
    fig, ax = plot_plt_radar(values[0], labels, color=color_order_list[0])
    ax.radar_plot.set_label(legend_labels_list[0])
    angles = calc_axis_angles(len(labels))

    for i, val in enumerate(values[1:]):
        radar = plot_values(ax, angles=angles, values=val, color=color_order_list[i + 1])
        radar.set_label(legend_labels_list[i + 1])
    fig.legend(prop={'size': 10})
    return fig, ax
