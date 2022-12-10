import os
import gc
import warnings

from settings import FIGURES_DIR, REPORTS_DIR, USE_DUMMY
from src.features.data_loaders import load_optimisation_data
from src.visualization.plots.energy_comparison_plots import save_player_matches_plots
from src.visualization.helpers.processing import parse_all_iterations_df, get_best_iteration, get_iteration_power_score

import matplotlib
import pandas as pd

# memory error issue: https://github.com/open-mmlab/mmdetection/issues/7035
matplotlib.use('Agg')
# keep clean terminal
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None

players_gps_score_df = load_optimisation_data(is_dummy=USE_DUMMY)
all_players = players_gps_score_df.athlete.unique()

for player in all_players:
    print(f'Processing: {player}')
    player_matches = players_gps_score_df[players_gps_score_df.athlete == player]

    methods = ['pso', 'nelder-mead']
    for method in methods:
        save_path = os.path.join(FIGURES_DIR, method, player)
        load_path = os.path.join(REPORTS_DIR, method, player)
        all_df = pd.read_csv(os.path.join(load_path, 'all_iterations_df.csv'))
        all_df = parse_all_iterations_df(all_df)

        best_it_series = get_best_iteration(all_df)
        pd_rv = get_iteration_power_score(best_it_series)
        save_player_matches_plots(player_matches, pd_rv, save_path)
        gc.collect()
