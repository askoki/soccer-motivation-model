import os
import warnings

from settings import FIGURES_DIR, USE_DUMMY
from src.features.data_loaders import load_optimisation_data
from src.features.file_helpers import create_dir
from src.visualization.constants import LIGHT_RED
from src.visualization.helpers.format_converters import convert_power_score_confidence_to_matplotlib_format
from src.visualization.helpers.processing import generate_error_per_gd_for_method, get_max_err_series
from src.visualization.plots.radar_plots import plot_plt_radar

import pandas as pd
import matplotlib.pyplot as plt

# keep clean terminal
warnings.simplefilter(action='ignore', category=FutureWarning)

players_gps_score_df = load_optimisation_data(is_dummy=USE_DUMMY)
pso_err_df = generate_error_per_gd_for_method('pso', players_gps_score_df)
nelder_err_df = generate_error_per_gd_for_method('nelder-mead', players_gps_score_df)

pso_max_s = get_max_err_series(pso_err_df)
nelder_max_s = get_max_err_series(nelder_err_df)


def generate_power_score_confidence_radar(method_df: pd.DataFrame, save_path_dir: str):
    method_max_s = get_max_err_series(method_df)
    max_players = method_df.shape[0]
    curr_player = 0
    for idx, player_row in method_df.iterrows():
        player_name = player_row.player
        curr_player += 1
        print(f'{curr_player}/{max_players}')
        save_path = os.path.join(save_path_dir, player_name)
        create_dir(save_path)
        labels, values = convert_power_score_confidence_to_matplotlib_format(method_max_s, player_row)
        fig, ax = plot_plt_radar(values, labels, color=LIGHT_RED)
        fig.savefig(os.path.join(save_path, 'power_score_confidence_radar.png'), dpi=300)
        plt.close()


methods = [('pso', pso_err_df), ('nelder-mead', nelder_err_df)]
for method, method_df in methods:
    print(method)
    save_path = os.path.join(FIGURES_DIR, method)
    generate_power_score_confidence_radar(method_df, save_path)
