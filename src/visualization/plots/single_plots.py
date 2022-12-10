import pandas as pd
from src.features.score.helpers import PowerScore
import matplotlib.pyplot as plt

from src.visualization.helpers.matplotlib_style import load_plt_style
from src.visualization.helpers.processing import create_player_error_per_gd_df


def visualize_estimated_power(power_descriptor: PowerScore) -> plt.Figure:
    load_plt_style()
    fig = plt.figure(figsize=(6, 3))
    plt.title('Power distribution')
    score_values = [int(x) for x in list(power_descriptor.name_dict.keys())]
    power_list = [power_descriptor.name_dict[str(x)] for x in score_values]

    stamina_value = power_descriptor.get_input_vector()[-1]
    plt.bar(score_values, power_list)
    plt.ylabel('Power')
    plt.xlabel(f'Score difference [stamina_factor={stamina_value}]')
    return fig


def plot_player_error_per_score_bar(power_desc: PowerScore, player_score_df: pd.DataFrame) -> plt.Figure:
    load_plt_style()
    power_params = power_desc.name_dict.keys()
    param_errors = []
    err_player_df = create_player_error_per_gd_df(power_desc, player_score_df)

    for i, param in enumerate(power_params):
        param_errors.append(err_player_df.loc[:, f'err_{param}'].iloc[0])

    fig = plt.figure(figsize=(8, 5.5))
    plt.title('Error per score')
    plt.bar(power_params, param_errors)
    plt.ylabel('Error')
    plt.xlabel('GD')
    return fig


def plot_player_score_minute(power_desc: PowerScore, player_score_df: pd.DataFrame) -> plt.Figure:
    load_plt_style()
    power_params = power_desc.name_dict.keys()
    param_errors = []

    for i, param in enumerate(power_params):
        score_gps = player_score_df[player_score_df.score_diff == int(param)]
        minutes_for_the_score = score_gps.duration_min.sum()
        param_errors.append(minutes_for_the_score)

    fig = plt.figure(figsize=(8, 5.5))
    plt.title('Minutes per GD')
    plt.bar(power_params, param_errors)
    plt.ylabel('Minutes cumulative')
    plt.xlabel('GD')
    return fig


def plot_best_run(power_desc: PowerScore, error_iterations_list: list):
    # first get the best
    best_iteration = error_iterations_list[0]
    for iteration in error_iterations_list:
        if iteration.fun < best_iteration.fun:
            best_iteration = iteration

    iteration_step_details = best_iteration.allvecs
    param_dict = {}
    parameters = power_desc.get_input_names()
    for i, param in enumerate(parameters):
        param_dict[param] = [(lambda r, i: r[i])(r, i) for r in iteration_step_details]

    fig = plt.figure(figsize=(8, 4))
    plt.ylabel('Error')
    plt.xlabel('Iteration')
    for i, param in enumerate(parameters):
        plt.title('Best run')
        plt.plot(range(len(iteration_step_details)), param_dict[param], label=param)
        plt.legend()
    return fig
