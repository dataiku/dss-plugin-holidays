import logging
import os
import pandas as pd
from dateutil import parser
import datetime


logging.basicConfig(level=logging.INFO,  format='Bank holidays plugin %(levelname)s - %(message)s')

# since we're working on ROW mode, a full dict is generated. Column names are generated
# dynamically since we don't want to cause override of existing columns in case "is_holiday" and/or
# "holiday_reason" already exist in the dataset.
SET_COLUMN_NAMES = True
IS_HOLIDAY_COLUMN = None
HOLIDAY_REASON_COLUMN = None

# TODO find a better way of doing this!!! when the processor starts it does so under the tmp folder, not the plugin folder...
folders = ['installed', 'dev']
for folder in folders:
    file_dir = os.path.join(os.environ['DIP_HOME'], 'plugins/{}/holidays/resources/holidays_calendar.csv'.format(folder))
    try:
        df = pd.read_csv(file_dir)
        df['date'] = df['date'].astype('datetime64')
    except IOError:
        None


def generate_next_column_name(columns, column):
    """
    given a list of columns and a desired column name, it will check if the name is taken, if so it will
    append suffixes to the name until finding one that's available.
    """
    if column not in columns:
        return column
    else:
        new_column_name = column
        i=1
        while new_column_name in columns:
            new_column_name = column + '_{}'.format(i)
            i+=1
        return new_column_name


def process(row):
    # needed to avoid a UnboundLocalError
    global SET_COLUMN_NAMES
    global IS_HOLIDAY_COLUMN
    global HOLIDAY_REASON_COLUMN

    selected_column = params.get('column')
    selected_country = params.get('country')
    extract_name = params.get('extract_name')

    # this should catch cases where the parser fails (for example NoneType input).
    # I'm setting the parsed_input to be a dummy date which will not render any results.
    # TODO confirm methodology or implement more accepted one.
    try:
        parsed_input = parser.parse(row.get(selected_column), ignoretz=True)
    except TypeError:
        parsed_input = pd.Timestamp.min
    is_holiday = df[(df['country_iso']==selected_country) & (df['date']==parsed_input)]

    # There might be a better way if one could access the dataset from outside the process method?
    if SET_COLUMN_NAMES is True:
        IS_HOLIDAY_COLUMN = generate_next_column_name(row.columns, "{}_holiday_bank".format(selected_column))
        HOLIDAY_REASON_COLUMN = generate_next_column_name(row.columns, "{}_holiday_bank_reasons".format(selected_column))
        SET_COLUMN_NAMES = False

    if extract_name is True:
        row[IS_HOLIDAY_COLUMN] = bool(is_holiday.shape[0])
        row[HOLIDAY_REASON_COLUMN] = next(iter(is_holiday.holiday_reason.tolist()), None)
    else:
        row[IS_HOLIDAY_COLUMN] = bool(is_holiday.shape[0])
    return row