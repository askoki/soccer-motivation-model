import os
import sys
import time
from typing import List

import pandas as pd
import scipy.optimize as opt
from random import randint
from settings import NELDER_MEAD_DIR, USE_DUMMY
from src.features.data_loaders import load_optimisation_data
from src.features.file_helpers import create_dir
from src.features.optimisation.processing import fun_min
from src.features.optimisation.results_helpers import SubIterationResult
from src.features.score.helpers import PowerScore, create_iteration_results_df
from src.models.constants import initial_power_vector, NUM_ITERATIONS, bounds_power, bounds_stamina

players_gps_score_df = load_optimisation_data(is_dummy=USE_DUMMY)

create_dir(NELDER_MEAD_DIR)
players_opt_power_df = pd.DataFrame()
players_list = players_gps_score_df.athlete.unique()
players_count = len(players_list)


# needed for nelder-mead
def generate_initial_vector():
    init_power = randint(bounds_power[0], bounds_power[1])
    init_vect: List[float] = [init_power for _ in range(len(initial_power_vector))]
    init_stamina_factor = randint(bounds_stamina[0] * 10, bounds_stamina[1] * 10) / 10.0
    init_vect.append(init_stamina_factor)
    return init_vect


for i, player_name in enumerate(players_list):
    print(f'Processing player: {player_name} {i + 1}/{players_count}')

    player_save_name = player_name.replace(' ', '_')
    save_path = os.path.join(NELDER_MEAD_DIR, player_save_name)
    create_dir(save_path)

    # OPTIMISATION PROCESS
    player_matches = players_gps_score_df[players_gps_score_df.athlete == player_name]
    results = []
    complete_results = []

    bounds = [bounds_power for i in range(len(initial_power_vector))]
    bounds.append(bounds_stamina)

    start = time.time()
    all_iterations_df = pd.DataFrame()
    for j in range(NUM_ITERATIONS):
        print(f'Iteration {j + 1} for all games')
        # init score
        init_vector = generate_initial_vector()
        power_desc = PowerScore(init_vector[:-1], init_vector[-1])
        input_vector = power_desc.get_input_vector()

        sub_it_res = SubIterationResult()
        result = opt.minimize(
            fun_min, input_vector,
            args=(player_matches, sub_it_res),
            bounds=bounds,
            method='Nelder-Mead',
            options={'return_all': True},
        )
        iteration_df = create_iteration_results_df(
            it_count=j, init_params=str(init_vector),
            num_steps=result.nit, num_eval=result.nfev,
            res_vect=str(result.x), fin_cost_fun=result.fun
        )
        # inner iteration results
        opt_variable_vectors_df = pd.DataFrame(result.allvecs, columns=['P-2', 'P-1', 'P0', 'P1', 'P2', 'stamina'])
        opt_variable_vectors_df.to_csv(os.path.join(save_path, f'iteration_{j}_opt_variable_steps.csv'), index=False)

        cost_function_df = pd.DataFrame(sub_it_res.get_func_list(), columns=['cost_fun'])
        cost_function_df.loc[:, 'num_eval'] = [x + 1 for x in range(sub_it_res.evaluation_count)]
        cost_function_df.to_csv(os.path.join(save_path, f'iteration_{j}_cost_fun_evaluations.csv'), index=False)

        all_iterations_df = pd.concat([all_iterations_df, iteration_df])
        results.append(result.x)
        complete_results.append(result)

    all_iterations_df.to_csv(os.path.join(save_path, 'all_iterations_df.csv'), index=False)
    end = time.time()
    print(f'Time for optimisation: {end - start}')
