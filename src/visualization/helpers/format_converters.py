import pandas as pd
import numpy as np

from settings import ETA_SIGN, ERROR_SIGN
from src.features.score.helpers import PowerScore
from src.models.constants import bounds_power, bounds_stamina
from src.visualization.helpers.processing import error_columns


def convert_power_score_to_matplotlib_format(ps: PowerScore) -> tuple:
    score_v = ps.get_power_vector()
    # (x) / (max)
    score_v = score_v / bounds_power[1] * 100
    stamina_factor = (ps.stamina / bounds_stamina[1]) * 100
    list_labels = [
        '$P_0$',
        '$P_1$',
        '$P_2$',
        ETA_SIGN,
        '$P_{-2}$',
        '$P_{-1}$',
    ]
    list_values = [
        score_v[2],
        score_v[3],
        score_v[4],
        stamina_factor,
        score_v[0],
        score_v[1],
        # repeat 1st value to close the graph
        score_v[2],
    ]
    return list_labels, list_values


def convert_power_score_confidence_to_matplotlib_format(max_s: pd.Series, player_s: pd.Series) -> tuple:
    confidence_s = pd.Series(dtype=float)
    max_error = max_s.max()

    for col in error_columns:
        if player_s.loc[col] < 0:
            confidence_s.loc[col] = 0
            continue
        player_s.loc[col] = max_error if np.isnan(player_s.loc[col]) else player_s.loc[col]
        confidence_s.loc[col] = (1 - player_s.loc[col] / max_error) * 100

    list_labels = [
        f'${ERROR_SIGN}_0$',
        f'${ERROR_SIGN}_1$',
        f'${ERROR_SIGN}_2$',
        f'${ERROR_SIGN}_{{TOT}}$',
        f'${ERROR_SIGN}_{{{-2}}}$',
        f'${ERROR_SIGN}_{{{-1}}}$',
    ]
    list_values = [
        confidence_s.loc['err_0'],
        confidence_s.loc['err_1'],
        confidence_s.loc['err_2'],
        confidence_s.loc['err_total'],
        confidence_s.loc['err_-2'],
        confidence_s.loc['err_-1'],
        # repeat 1st value to close the graph
        confidence_s.loc['err_0'],
    ]
    return list_labels, list_values
