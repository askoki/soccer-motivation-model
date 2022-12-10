import os
import gc
import time
import functools
import pandas as pd
from indago import PSO
from src.features.data_loaders import load_optimisation_data
from src.features.optimisation.results_helpers import SubIterationResult
from src.features.score.helpers import PSOResults, create_iteration_results_df
from src.features.file_helpers import create_dir
from src.features.optimisation.processing import fun_min
from src.features.score.helpers import PowerScore
from src.models.constants import initial_stamina_factor, NUM_ITERATIONS, initial_power_vector, bounds_power, \
    bounds_stamina
from settings import PSO_DIR, USE_DUMMY

players_gps_score_df = load_optimisation_data(is_dummy=USE_DUMMY)


def post_iteration_processing(it, candidates, best, iteration_dict: {}):
    if candidates[0] <= best:
        iteration_dict['X'].append(candidates[0].X)
        iteration_dict['f'].append(candidates[0].f)
    return


create_dir(PSO_DIR)
players_opt_power_df = pd.DataFrame()
players_list = players_gps_score_df.athlete.unique()
players_count = len(players_list)
iteration_results_list = []

if __name__ == '__main__':
    for i, player_name in enumerate(players_list):
        print(f'Processing player: {player_name} {i + 1}/{players_count}')

        player_save_name = player_name.replace(' ', '_')
        save_path = os.path.join(PSO_DIR, player_save_name)
        create_dir(save_path)

        # init score
        power_desc = PowerScore(initial_power_vector, initial_stamina_factor)
        input_vector = power_desc.get_input_vector()

        # OPTIMISATION PROCESS
        player_matches = players_gps_score_df[players_gps_score_df.athlete == player_name]
        results = []
        complete_results = []
        gc.collect()

        start = time.time()
        all_iterations_df = pd.DataFrame()
        for j in range(NUM_ITERATIONS):
            print(f'Iteration {j + 1} for all games')
            optimizer = PSO()
            iteration_dict = {
                'iteration': j,
                'X': [],
                'f': []
            }
            post_iteration_function = functools.partial(post_iteration_processing, iteration_dict=iteration_dict)
            optimizer.post_iteration_processing = post_iteration_function
            optimizer.number_of_processes = 1
            optimizer.monitoring = 'dashboard'
            optimizer.maximum_stalled_iterations = 100

            lb_vector = [bounds_power[0] for i in range(len(initial_power_vector))]
            lb_vector.append(bounds_stamina[0])

            optimizer.dimensions = len(lb_vector)
            optimizer.lb = lb_vector
            ub_vector = [bounds_power[1] for i in range(len(initial_power_vector))]
            ub_vector.append(bounds_stamina[1])
            optimizer.ub = ub_vector

            sub_it_res = SubIterationResult()
            evaluation_function = functools.partial(
                fun_min,
                player_all_games_score_df=player_matches,
                sub_result=sub_it_res
            )
            optimizer.evaluation_function = evaluation_function
            result = optimizer.optimize()

            iteration_results_list.append(iteration_dict)
            it_results = PSOResults(
                x=result.X,
                fun=result.f,
                allvecs=iteration_dict['X']
            )
            complete_results.append(it_results)
            results.append(result.X)

            iteration_df = create_iteration_results_df(
                it_count=j, init_params=str(input_vector),
                num_steps=optimizer.it, num_eval=optimizer.eval,
                res_vect=str(result.X), fin_cost_fun=result.f
            )
            opt_variable_vectors_df = pd.DataFrame(
                iteration_dict['X'], columns=['P-2', 'P-1', 'P0', 'P1', 'P2', 'stamina']
            )
            opt_variable_vectors_df.to_csv(
                os.path.join(save_path, f'iteration_{j}_opt_variable_steps.csv'), index=False
            )

            cost_function_df = pd.DataFrame(sub_it_res.get_func_list(), columns=['cost_fun'])
            cost_function_df.loc[:, 'num_eval'] = [x + 1 for x in range(sub_it_res.evaluation_count)]
            cost_function_df.to_csv(os.path.join(save_path, f'iteration_{j}_cost_fun_evaluations.csv'), index=False)
            all_iterations_df = pd.concat([all_iterations_df, iteration_df])

        all_iterations_df.to_csv(os.path.join(save_path, 'all_iterations_df.csv'), index=False)
        end = time.time()
        print(f'Time for optimisation: {end - start}')
