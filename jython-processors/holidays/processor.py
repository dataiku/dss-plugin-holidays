 # -*- coding: utf-8 -*-
import logging
# import matcher
import pandas as pd
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,  # avoid getting log from 3rd party module
                    format='Anonymization plugin %(levelname)s - %(message)s')


file_dir = (os.path.abspath(os.path.join(os.path.dirname("__file__"), '../..')) + '/resources')
df = pd.read_csv(os.path.join(file_dir, 'holidays_calendar.csv'))
df['date'] = df['date'].astype('datetime64')


def process(row):
    selected_column = params.get('column')
    selected_country = params.get('country')
    extract_name = params.get('extract_name')
    return type(row.get(selected_column))