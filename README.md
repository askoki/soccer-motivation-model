football-motivation-optimisation
==============================

A short description of the project.

Project Organization
------------

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    │
    ├── scripts             <- Scripts for optimisation and plot generation.
    │   ├── start_optimisation.sh        
    │   └── generate_all_plots.sh
    │
    ├── reports            <- Generated analysis as csv, png, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── features       <- Helper scripts for optimisation and processing
    │   │
    │   ├── models         <- Scripts to start optimisation
    │   │   ├── nelder-mead
    │   │   │   └── optimize.py
    │   │   ├── pso
    │   │   │   └── optimize.py
    │   │   └── constants.py
    │   │  
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       ├── generate_power_alpha_radars.py
    │       ├── generate_power_score_confidence_radars.py
    │       ├── generate_error_per_score_per_min_n_power_score_minute.py
    │       ├── generate_cost_fun_through_it.py
    │       ├── generate_cost_fun_through_eval.py
    │       ├── generate_best_iteration_var_convergence.py
    │       ├── create_player_energy_comparison_plots.py
    │       ├── gen_allin1_power_alpha.py
    │       └── combine_all_plots.py
    │
    └── settings.py            <- Project related configuration and settings.

--------
