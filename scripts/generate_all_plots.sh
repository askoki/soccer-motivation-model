#!/usr/bin/env bash

sh -c 'cd ../src/visualization && python generate_power_score_confidence_radars.py'
sh -c 'cd ../src/visualization && python generate_power_alpha_radars.py'
sh -c 'cd ../src/visualization && python generate_error_per_score_per_min_n_power_score_minute.py'
sh -c 'cd ../src/visualization && python generate_cost_fun_through_it.py'
sh -c 'cd ../src/visualization && python generate_cost_fun_through_eval.py'
sh -c 'cd ../src/visualization && python generate_best_iteration_var_convergence.py'
sh -c 'cd ../src/visualization && python create_player_energy_comparison_plots.py'
sh -c 'cd ../src/visualization && python gen_allin1_power_alpha.py'
sh -c 'cd ../src/visualization && python combine_all_plots.py'
