import functools

import pandas as pd
import numpy as np
from src.features.optimisation.results_helpers import SubIterationResult
from src.features.score.helpers import PowerScore


def calc_energy_expenditure_from_initial_power(gps_score_df: pd.DataFrame, power_descriptor: PowerScore) -> np.array:
    # power vector: -2, -1, 0, 1, 2, 3, 4
    gps_score_df.loc[:, 'estimated_power'] = gps_score_df['score_diff'].apply(
        lambda x: power_descriptor.name_dict[str(x)]
    )
    fatigue_effect = calc_fatigue_effect(power_descriptor.stamina, gps_score_df.loc[:, 'min_from_start'])
    gps_score_df.loc[:, 'estimated_energy_pm'] = gps_score_df['estimated_power'] * gps_score_df[
        'duration_min'] * fatigue_effect
    return np.array(gps_score_df.loc[:, 'estimated_energy_pm'].copy())


def exponential_decay_fatigue_function(time: int, coefficient: float) -> float:
    return np.exp(-time * coefficient)


def calc_fatigue_effect(stamina_factor: float, min_from_start_array: np.array) -> np.array:
    FULL_GAME_DURATION = 90
    alpha = -np.log(stamina_factor) / FULL_GAME_DURATION
    calc_fatigue = functools.partial(exponential_decay_fatigue_function, coefficient=alpha)
    fatigue_influence = np.array(list(map(calc_fatigue, min_from_start_array)))
    return fatigue_influence


def fun_min(input_vector, player_all_games_score_df: pd.DataFrame, sub_result: SubIterationResult or None):
    power_descriptor = PowerScore(input_vector[:-1], stamina=input_vector[-1])
    cum_error = 0
    all_matches_duration = 0
    for idx, game_df in player_all_games_score_df.groupby('date'):
        energy_real = game_df['energy (J/kg)'].cumsum().to_numpy()
        match_duration = game_df.duration_min.sum()
        time_x = game_df.duration_min.cumsum().to_numpy()
        time_x = np.insert(time_x, 0, 0)
        en_real = np.insert(energy_real, 0, 0)
        energy_calc = calc_energy_expenditure_from_initial_power(game_df, power_descriptor)
        en_calc = energy_calc.cumsum()
        en_calc = np.insert(en_calc, 0, 0)
        en_calc = np.insert(en_calc, 0, 0)
        game_error = 0
        for i in range(time_x.shape[0] - 1):
            start_idx = i
            # end border is not included (+1)
            end_idx = i + 2
            en_calc_val = np.trapz(en_calc[start_idx:end_idx], time_x[start_idx:end_idx])
            en_real_val = np.trapz(en_real[start_idx:end_idx], time_x[start_idx:end_idx])
            error = (en_real_val - en_calc_val) ** 2
            game_error += error
        all_matches_duration += match_duration
        cum_error += game_error
    cum_error /= all_matches_duration
    if sub_result is not None:
        sub_result.add_sub_iteration_result(cum_error)
    return cum_error
