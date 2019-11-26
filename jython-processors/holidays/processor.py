import logging
import os
import pandas as pd
from dateutil import parser
import datetime


logging.basicConfig(level=logging.INFO,  format='Holidays plugin %(levelname)s - %(message)s')

folders = ['installed', 'dev']
for folder in folders:
    file_path = os.path.join(os.environ['DIP_HOME'], 'plugins/{}/holidays/resources/holidays_calendar.csv'.format(folder))
    if os.path.exists(file_path) is True:
        df = pd.read_csv(file_path)
        df['date'] = df['date'].astype('datetime64')

# TODO maybe a better way of handling the case where the resources file is not found in either folder.
# Like if someone forgot to upload it to git(?)
try:
    df
except Exception as e:
    logging.info("Creating an empty dataframe as file was not found.")
    df = pd.DataFrame(columns=['country_iso', 'date', 'holiday_reason'])


def process(row):
    input_column = params.get('input_column')
    country = params.get('country')
    output_holiday_name = params.get('output_holiday_name')

    try:
        parsed_input = parser.parse(row.get(input_column), ignoretz=True)
    except Exception as e:
        parsed_input = pd.Timestamp.min
        logging.info("Error parsing input date, using dummy date.")

    is_holiday = df[(df['country_iso']==country) & (df['date']==parsed_input)]

    if output_holiday_name is True:
        row["is_holiday"] = bool(is_holiday.shape[0])
        row["holiday_name"] = next(iter(is_holiday.holiday_reason.tolist()), None)
    else:
        row["is_holiday"] = bool(is_holiday.shape[0])
    return row