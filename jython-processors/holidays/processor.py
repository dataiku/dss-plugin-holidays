import logging
import os
import pandas as pd
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,  # avoid getting log from 3rd party module
                    format='Anonymization plugin %(levelname)s - %(message)s')

# TODO find a better way of doing this!!! when the processor starts it does so under the tmp folder, not the plugin folder...
file_dir = (os.path.abspath(os.path.join(os.path.dirname("__file__"), '../../..')) + '/plugins/dev/bank_holidays/resources')
# this is when one assumes the path is relative to the plugin itself
# file_dir = (os.path.abspath(os.path.join(os.path.dirname("__file__"), '../..')) + '/resources')

df = pd.read_csv(os.path.join(file_dir, 'holidays_calendar.csv'))
df['date'] = df['date'].astype('datetime64')

def process(row):
    selected_column = params.get('column')
    selected_country = params.get('country')
    extract_name = params.get('extract_name')

    # filtering part. Not 100% sure how to determine if the column used as param is indeed a date.
    # also want to check for cases where the date matches, but the hours or mins not zeroes
    is_holiday = df[(df['country_iso']==selected_country) & (df['date']==row.get(selected_column))]

    # to keep consistent with the other processor, if the user has selected to retrieve the name of the
    # holiday, then we make a list. However, it's unclear how to create two columns from here.
    # ideally this would be one column if the user doesn't want to know the name of the holiday, and two columns
    if extract_name:
        results = is_holiday.holiday_reason.tolist()
        return [bool(is_holiday.shape[0]), next(iter(is_holiday.holiday_reason.tolist()), None)]
    else:
        return bool(is_holiday.shape[0])