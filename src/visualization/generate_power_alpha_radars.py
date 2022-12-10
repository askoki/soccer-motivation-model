import os
import warnings

from settings import FIGURES_DIR, REPORTS_DIR, USE_DUMMY
from src.features.data_loaders import load_optimisation_data
from src.visualization.helpers.format_converters import convert_power_score_to_matplotlib_format
from src.visualization.helpers.processing import parse_all_iterations_df, get_best_iteration, get_iteration_power_score
from src.visualization.plots.radar_plots import plot_plt_radar

import pandas as pd
import matplotlib.pyplot as plt

# keep clean terminal
warnings.simplefilter(action='ignore', category=FutureWarning)

players_gps_score_df = load_optimisation_data(is_dummy=USE_DUMMY)
all_players = players_gps_score_df.athlete.unique()

for player in all_players:
    print(f'Processing: {player}')
    player_matches = players_gps_score_df[players_gps_score_df.athlete == player]

    methods = ['pso', 'nelder-mead']
    for method in methods:
        save_path = os.path.join(FIGURES_DIR, method, player)
        all_df = pd.read_csv(os.path.join(REPORTS_DIR, method, player, 'all_iterations_df.csv'))
        all_df = parse_all_iterations_df(all_df)

        best_it_series = get_best_iteration(all_df)
        pd_rv = get_iteration_power_score(best_it_series)

        labels, values = convert_power_score_to_matplotlib_format(pd_rv)
        fig, ax = plot_plt_radar(values, labels)
        fig.savefig(os.path.join(save_path, "power_score_radar.png"), dpi=300)
        plt.close()
