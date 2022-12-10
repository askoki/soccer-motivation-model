import os
import gc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.features.optimisation.processing import calc_energy_expenditure_from_initial_power
from src.features.score.helpers import PowerScore
from src.visualization.helpers.matplotlib_style import load_plt_style


def plot_energy_comparison(gps_score_df: pd.DataFrame, power_descriptor: PowerScore) -> plt.Figure:
    load_plt_style()
    energy_real = gps_score_df['energy (J/kg)'].cumsum()
    energy_calc = calc_energy_expenditure_from_initial_power(gps_score_df, power_descriptor).cumsum()
    x_axis = gps_score_df.min_from_start

    linewidth = 3

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6), sharex=True)
    # fig.patch.set_facecolor('white')

    # ax1.set_facecolor('xkcd:white')
    ax1.set_title(f'Energy comparison')
    ax1.plot(x_axis, energy_real, color='steelblue', label='Real expenditure', linewidth=linewidth)
    ax1.plot(x_axis, energy_calc, color='orange', label='Calculated expenditure', linewidth=linewidth)
    ax1.set_xlabel('Game time (min)')
    ax1.set_ylabel('Cum. energy expenditure (J/kg)')
    ax1.set_ylim(0, 55000)

    score_diff_list = [int(x) for x in gps_score_df.score_diff.values]
    ax2.plot(x_axis, score_diff_list, color='gray', label='GD', linewidth=linewidth)
    ax2.set_xlabel('Game time (min)')
    ax2.set_ylabel('GD')
    ax2.set_title(f'GD margin')
    # ax2.set_facecolor('xkcd:white')
    ax2.set_yticks(np.arange(-2, 3))

    ax3.plot(x_axis, gps_score_df.estimated_power, color='lightblue', label='Estimated power', linewidth=linewidth)
    ax3.set_xlabel('Game time (min)')
    ax3.set_ylabel('Power (W)')
    ax3.set_title(f'Estimated GD dependent power')
    ax3.set_ylim(600, 800)
    # ax3.set_facecolor('xkcd:white')

    if any([s < 0 for s in score_diff_list]):
        fig.legend(loc='right', bbox_to_anchor=(0.9, 0.6))
    else:
        fig.legend(loc='right', bbox_to_anchor=(0.9, 0.25))
    return fig


def save_player_matches_plots(player_matches_df: pd.DataFrame, p_desc: PowerScore, save_path: str):
    player_save_name = player_matches_df.iloc[0].athlete.replace(' ', '_')
    for game in player_matches_df.groupby('date'):
        index, game_df = game
        fig = plot_energy_comparison(game_df, p_desc)
        game_date = game_df.iloc[0].date
        fig.savefig(os.path.join(save_path, f'{player_save_name}_{game_date}.png'))
        plt.close()
        plt.close("all")
        plt.close()
        gc.collect()