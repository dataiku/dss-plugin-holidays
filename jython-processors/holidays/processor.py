import logging
import os
import pandas as pd
from dateutil import parser
import datetime
import json

logging.basicConfig(level=logging.INFO,  format='Holidays plugin %(levelname)s - %(message)s')
folders = ['installed', 'dev']


def get_file_path(file_name):
    for folder in folders:
        file_path = os.path.join(os.environ['DIP_HOME'], 'plugins/{}/holidays/resources/{}'.format(folder, file_name))
        if os.path.exists(file_path) is True:
            return file_path
    return None


def load_or_create_dataframe(file_name, columns):

    file_path = get_file_path(file_name)
    if file_path is None:
        df = pd.DataFrame(columns=columns, index_col=index_col)
        logging.info("Creating an empty dataframe as file was not found.")
    else:
        df = pd.read_csv(file_path)
    return df


holidays_df = load_or_create_dataframe("holidays_calendar.csv", columns=["country_name","country_iso","date","holiday_reason"])
holidays_df['date'] = holidays_df['date'].astype('datetime64')
weekends_df = load_or_create_dataframe("weekends.csv", columns=["country_name","country_iso","weekend_day_numbers"])


def process(row):
    input_column = params.get('input_column')
    country = params.get('country')
    output_holiday_name = params.get('output_holiday_name')
    flag_weekends = params.get('flag_weekends')

    try:
        parsed_input = parser.parse(row.get(input_column), ignoretz=True)
        day_of_the_week = parsed_input.weekday()
    except Exception as e:
        parsed_input = pd.Timestamp.min
        logging.info("Error parsing input date, using dummy date.")

    is_holiday = holidays_df[(holidays_df.country_iso==country) & (holidays_df.date==parsed_input)]

    row["is_holiday"] = bool(is_holiday.shape[0])
    if output_holiday_name is True:
        row["holiday_name"] = next(iter(is_holiday.holiday_reason.tolist()), None)

    if flag_weekends is True:
        weekend_days = json.loads(next(iter(weekends_df.weekend_day_numbers.tolist()), None))
        row["is_weekend"] = day_of_the_week in weekend_days

    return row