import os
import warnings

from settings import FIGURES_DIR, USE_DUMMY, REPORTS_DIR
from src.features.data_loaders import load_optimisation_data
from src.models.constants import NUM_ITERATIONS
from src.visualization.helpers.matplotlib_style import load_plt_style
from src.visualization.helpers.processing import parse_all_iterations_df

import numpy as np
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

        load_plt_style()
        fig = plt.figure(figsize=(10, 6))
        plt.ylabel('Cost function')
        plt.xlabel('Evaluations')
        plt.title('Cost function through evaluations')
        for i in range(NUM_ITERATIONS):
            keep_step = 10
            eval_df = pd.read_csv(os.path.join(load_path, f'iteration_{i}_cost_fun_evaluations.csv'))
            reduced_df = eval_df.iloc[::keep_step, :]
            plt.plot(reduced_df.num_eval.values, reduced_df.cost_fun.values, label=f'Iteration {i + 1}')
        plt.yscale('log')
        plt.legend()
        fig.savefig(os.path.join(save_path, 'cost_function_through_evaluations.png'), dpi=300)
        plt.close()
