import os
import pandas as pd
from settings import REPORTS_DIR
from src.features.optimisation.processing import fun_min
from src.features.score.helpers import PowerScore


def create_player_error_per_gd_df(power_desc: PowerScore, df: pd.DataFrame) -> pd.DataFrame:
    power_params = power_desc.name_dict.keys()
    err_df = pd.DataFrame({
        'player': df.iloc[0].athlete
    }, index=[0])

    for i, param in enumerate(power_params):
        score_gps = df[df.score_diff == int(param)]
        if score_gps.empty:
            score_err = -1
        else:
            score_err = fun_min(power_desc.get_input_vector(), score_gps, sub_result=None)
        err_df.loc[:, f'err_{param}'] = score_err
    # Add total error for player
    total_err = fun_min(power_desc.get_input_vector(), df, sub_result=None)
    err_df.loc[:, f'err_total'] = total_err
    assert err_df.shape[0] == 1
    return err_df


def generate_error_per_gd_for_method(method: str, df: pd.DataFrame) -> pd.DataFrame:
    err_df = pd.DataFrame()
    for player in df.athlete.unique():
        player_matches = df[df.athlete == player]

        data_path = os.path.join(REPORTS_DIR, method, player)
        all_df = pd.read_csv(os.path.join(data_path, 'all_iterations_df.csv'))
        all_df = parse_all_iterations_df(all_df)

        rv = get_best_iteration(all_df).resulting_vector.split(' ')
        # remove empty strings
        rv[:] = [x for x in rv if x]

        rv = [float(i) for i in rv]
        pd_rv = PowerScore(rv[:-1], rv[-1])

        err_player_df = create_player_error_per_gd_df(pd_rv, player_matches)
        err_df = pd.concat([err_df, err_player_df])
    err_df.reset_index(inplace=True, drop=True)
    return err_df


error_columns = ['err_-2', 'err_-1', 'err_0', 'err_1', 'err_2', 'err_total']


def get_max_err_series(err_df: pd.DataFrame) -> pd.Series:
    max_err_s = pd.Series(dtype=float)
    for col in error_columns:
        max_err_s.loc[col] = err_df[col].max()
    return max_err_s


def parse_all_iterations_df(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[:, 'resulting_vector'] = df.loc[:, 'resulting_vector'].str.replace('\n', '', regex=True)
    df.loc[:, 'resulting_vector'] = df.loc[:, 'resulting_vector'].str.replace('[', '', regex=True)
    df.loc[:, 'resulting_vector'] = df.loc[:, 'resulting_vector'].str.replace(']', '', regex=True)
    return df


def get_best_iteration(all_it_df: pd.DataFrame) -> pd.Series:
    return all_it_df.sort_values(['final_cost_function', 'number_of_evaluations'], ascending=True).iloc[0]


def get_iteration_power_score(best_it_series: pd.Series) -> PowerScore:
    rv = best_it_series.resulting_vector.split(' ')
    # remove empty strings
    rv[:] = [x for x in rv if x]

    rv = [float(i) for i in rv]
    return PowerScore(rv[:-1], rv[-1])
