import pandas as pd
import numpy as np


class PowerScore:
    def __init__(self, score_power_list: list, stamina=0.7):
        self.stamina = stamina
        self.name_dict = {
            '-2': score_power_list[0],
            '-1': score_power_list[1],
            '0': score_power_list[2],
            '1': score_power_list[3],
            '2': score_power_list[4],  # actually 2 or more
        }

    def get_power_vector(self) -> np.array:
        return np.array(list(self.name_dict.values()))

    def get_input_names(self, stamina_name: str = 'stamina') -> np.array:
        dict_names = list(self.name_dict.keys())
        dict_names.append(stamina_name)
        return np.array(dict_names)

    def get_input_vector(self) -> np.array:
        feature_list = list(self.name_dict.values())
        feature_list.append(self.stamina)
        return np.array(feature_list)


class PSOResults:

    def __init__(self, x: float, fun: float, allvecs: list):
        self.x = x
        self.fun = fun
        self.allvecs = allvecs


def create_iteration_results_df(it_count: int, init_params: str, num_steps: int, num_eval: int, res_vect: str,
                                fin_cost_fun: int) -> pd.DataFrame:
    return pd.DataFrame({
        'iteration_count': it_count,
        'init_params': init_params,
        'num_steps': num_steps,
        'number_of_evaluations': num_eval,
        'resulting_vector': res_vect,
        'final_cost_function': fin_cost_fun
    }, index=[it_count])
