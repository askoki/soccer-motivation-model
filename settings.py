import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

REPORTS_DIR = os.path.join(ROOT_DIR, 'reports')
NELDER_MEAD_DIR = os.path.join(REPORTS_DIR, 'nelder-mead')
PSO_DIR = os.path.join(REPORTS_DIR, 'pso')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')

USE_DUMMY = False
ETA_SIGN = u'\u03B7'
ERROR_SIGN = u'\u03B5'
