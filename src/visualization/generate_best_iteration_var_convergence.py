import os
import warnings

from settings import FIGURES_DIR, REPORTS_DIR, USE_DUMMY, ETA_SIGN
from src.features.data_loaders import load_optimisation_data
from src.models.constants import bounds_power
from src.visualization.helpers.matplotlib_style import load_plt_style
from src.visualization.helpers.processing import parse_all_iterations_df, get_best_iteration, get_iteration_power_score

import pandas as pd
import matplotlib.pyplot as plt

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

        load_plt_style()
        fig = plt.figure(figsize=(10, 6))
        plt.ylabel('Variable values')
        plt.xlabel('Iteration')
        plt.title('Best run')

        keep_step = 3
        best_it_df = pd.read_csv(
            os.path.join(load_path, f'iteration_{best_it_series.iteration_count}_opt_variable_steps.csv')
        )
        reduced_df = best_it_df.iloc[::keep_step, :]

        # to make columns equal names with PowerDict
        reduced_df.columns = reduced_df.columns.str.lstrip('P')

        # normalize values to fit on the same scale
        power_columns = pd_rv.name_dict.keys()
        for col in power_columns:
            reduced_df.loc[:, col] = (reduced_df.loc[:, col] - bounds_power[0]) / (bounds_power[1] - bounds_power[0])
        reduced_df = reduced_df.rename(columns={'stamina': ETA_SIGN})

        parameters = pd_rv.get_input_names(stamina_name=ETA_SIGN)
        for param in parameters:
            label_param = param
            if param != ETA_SIGN:
                label_param = f'$P_{{{param}}}$'
            plt.plot(reduced_df.index.values, reduced_df[param].values, label=label_param)
        plt.ylim(0, 1.1)
        plt.legend()
        fig.savefig(os.path.join(save_path, 'best_iteration_variables.png'), dpi=300)
        plt.close()
