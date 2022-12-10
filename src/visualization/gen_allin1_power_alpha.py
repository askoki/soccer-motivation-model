import os
import gc
import warnings

from settings import FIGURES_DIR, USE_DUMMY, REPORTS_DIR
from src.models.constants import position_dict
from src.features.data_loaders import load_optimisation_data
from src.visualization.plots.radar_plots import plot_plt_radar
from src.visualization.helpers.format_converters import convert_power_score_to_matplotlib_format
from src.visualization.helpers.processing import parse_all_iterations_df, get_best_iteration, get_iteration_power_score

import pandas as pd
import matplotlib.pyplot as plt

# keep clean terminal
warnings.simplefilter(action='ignore', category=FutureWarning)

players_gps_score_df = load_optimisation_data(is_dummy=USE_DUMMY)
players_gps_score_df.loc[:, 'athlete_id'] = players_gps_score_df.athlete.apply(lambda r: r.split('athlete')[1])
players_gps_score_df.loc[:, 'athlete_id'] = players_gps_score_df.loc[:, 'athlete_id'].astype(int)
all_players = players_gps_score_df.sort_values('athlete_id').athlete.unique()

methods = ['pso', 'nelder-mead']

for method in methods:
    nrows = 4
    ncols = 5

    fig, ax = plt.subplots(figsize=(20, 20), nrows=nrows, ncols=ncols, subplot_kw={'projection': 'polar'})
    row = 0
    col = 0
    save_path = os.path.join(FIGURES_DIR, method)

    for player in all_players:
        print(f'Processing: {player}')
        player_matches = players_gps_score_df[players_gps_score_df.athlete == player]
        player_path = os.path.join(REPORTS_DIR, method, player)
        all_df = pd.read_csv(os.path.join(player_path, 'all_iterations_df.csv'))
        all_df = parse_all_iterations_df(all_df)

        best_it_series = get_best_iteration(all_df)
        pd_rv = get_iteration_power_score(best_it_series)

        ax[row][col].set_title(position_dict[player])

        labels, values = convert_power_score_to_matplotlib_format(pd_rv)
        plot_plt_radar(values, labels, ax=ax[row][col])
        if (col % (ncols - 1) == 0) and (col > 0):
            row += 1
            col = 0
        else:
            col += 1

    ax[row][col].set_axis_off()

    fig.tight_layout()
    fig.savefig(os.path.join(save_path, 'all_players_power_score_radar.png'), dpi=300)
    plt.close()
    gc.collect()
