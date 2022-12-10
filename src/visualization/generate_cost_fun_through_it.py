import os
import warnings

from settings import FIGURES_DIR, REPORTS_DIR, USE_DUMMY
from src.features.optimisation.processing import fun_min
from src.features.score.helpers import PowerScore
from src.features.data_loaders import load_optimisation_data
from src.models.constants import NUM_ITERATIONS
from src.visualization.helpers.processing import parse_all_iterations_df

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

        fig = plt.figure(figsize=(16, 6))
        plt.ylabel('Cost function', fontsize='x-large')
        plt.xlabel('Iteration (inner)', fontsize='x-large')
        plt.title('Cost function through iterations', fontsize='x-large')
        for i in range(NUM_ITERATIONS):
            keep_step = 3
            it_df = pd.read_csv(os.path.join(load_path, f'iteration_{i}_opt_variable_steps.csv'))
            reduced_df = it_df.iloc[::keep_step, :]
            reduced_df.loc[:, 'cost_func'] = reduced_df.apply(
                lambda r:
                fun_min(
                    PowerScore([r['P-2'], r['P-1'], r['P0'], r['P1'], r['P2']], r.stamina).get_input_vector(),
                    player_matches,
                    sub_result=None
                ),
                axis=1
            )
            plt.plot(reduced_df.index.values, reduced_df.cost_func.values, label=f'Iteration {i + 1}')
        plt.legend()
        fig.savefig(os.path.join(save_path, 'cost_function_through_iterations.png'), dpi=300)
        plt.close()
