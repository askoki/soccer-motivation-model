import os
import gc

from settings import FIGURES_DIR, USE_DUMMY
from src.features.data_loaders import load_optimisation_data

import matplotlib.pyplot as plt
from matplotlib import image as mpimg

players_gps_score_df = load_optimisation_data(is_dummy=USE_DUMMY)
all_players = players_gps_score_df.athlete.unique()

for player in all_players:
    print(f'Processing: {player}')
    gc.collect()
    methods = ['pso', 'nelder-mead']
    for method in methods:
        save_path = os.path.join(FIGURES_DIR, method, player)
        err_p_score_p_min_img = mpimg.imread(os.path.join(save_path, 'error_per_score_per_minute.png'))
        p_score_radar = mpimg.imread(os.path.join(save_path, 'power_score_radar.png'))
        p_score_min_img = mpimg.imread(os.path.join(save_path, 'player_score_minute.png'))
        cost_fun_img = mpimg.imread(os.path.join(save_path, 'cost_function_through_evaluations.png'))
        best_it_img = mpimg.imread(os.path.join(save_path, 'best_iteration_variables.png'))
        confidence_radar_img = mpimg.imread(os.path.join(save_path, 'power_score_confidence_radar.png'))

        fig, ax = plt.subplots(3, 2, figsize=(20, 16))
        plt.subplots_adjust(hspace=0, wspace=0)
        fig.patch.set_facecolor('white')
        fig.suptitle('Player analysis', fontsize='x-large')
        fig.tight_layout()

        row1_col_1 = ax[0][0]
        row1_col_1.axis('off')
        row1_col_1.imshow(err_p_score_p_min_img)

        row1_col_2 = ax[0][1]
        row1_col_2.axis('off')
        row1_col_2.imshow(p_score_min_img)

        row2_col_1 = ax[1][0]
        row2_col_1.axis('off')
        row2_col_1.imshow(cost_fun_img)

        row2_col_2 = ax[1][1]
        row2_col_2.axis('off')
        row2_col_2.imshow(best_it_img)

        row1_col_3 = ax[2][0]
        row1_col_3.axis('off')
        row1_col_3.imshow(p_score_radar)

        row2_col_3 = ax[2][1]
        row2_col_3.axis('off')
        row2_col_3.imshow(confidence_radar_img)
        fig.savefig(os.path.join(save_path, 'optimisation_results_combined.png'), dpi=300)

        fig.clf()
        plt.close(fig)
        plt.close("all")
        plt.close()
        gc.collect()
    plt.close("all")
    plt.close()
    gc.collect()
