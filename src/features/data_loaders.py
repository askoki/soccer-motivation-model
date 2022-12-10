import os
import pandas as pd
from settings import PROCESSED_DATA_DIR

MAX_INTERVAL_MIN = 11


def load_optimisation_data(is_dummy=False):
    filename = 'data_df.csv'
    if is_dummy:
        filename = 'data_df_one_player.csv'
    df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, filename))
    return df
