import pandas as pd
import numpy as np

from utils.schema_def import ColNames
from utils.scoring import score_column



def find_vacations(df, threshold=5):
    # Sort the dataframe by technician name and event date
    df = df.sort_values(by=[ColNames.TECH_NAME, ColNames.EVENT_DATE])
    df[ColNames.EVENT_DATE] = pd.to_datetime(df[ColNames.EVENT_DATE], errors='coerce')
    df['data_end_date'] = pd.to_datetime(df['data_end_date'], errors='coerce')

    # Calculate the previous event date for each technician
    df['prev_event_date'] = df.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].shift(1)

    # Calculate the gap in days between consecutive events
    df['gap_days'] = np.where(
        pd.notna(df['prev_event_date']),
        (df[ColNames.EVENT_DATE] - df['prev_event_date']) / np.timedelta64(1, 'D'),
        np.nan
    )

    # Identify vacations based on the threshold
    df['vacation'] = df['gap_days'] > threshold

    # Get the last job date for each technician
    df['last_job_date'] = df.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('max')

    # Find the last vacation end date and its length for each technician
    df['last_vacation_end'] = df.groupby(ColNames.TECH_NAME)['prev_event_date'].transform(
        lambda x: x.where(df['vacation']).ffill()
    )
    df['vacation_length'] = df.groupby(ColNames.TECH_NAME)['gap_days'].transform(
        lambda x: x.where(df['vacation']).ffill()
    )

    # Calculate the days before the last job and the days before the end of the dataset
    df['time_since_vacation'] = np.where(
        pd.notna(df['last_vacation_end']),
        (df['last_job_date'] - df['last_vacation_end']) / np.timedelta64(1, 'D'),
        np.nan
    )

    df['days_before_data_end'] = np.where(
        pd.notna(df['last_vacation_end']),
        (df['data_end_date'] - df['last_vacation_end']) / np.timedelta64(1, 'D'),
        np.nan
    )

    # Filter to get the unique last vacation information for each technician
    result = df.drop_duplicates(subset=[ColNames.TECH_NAME], keep='last')[
        [ColNames.TECH_NAME, 'last_vacation_end', 'vacation_length', 'time_since_vacation', 'days_before_data_end']
    ].reset_index(drop=True)

    return result

def calc_vacation_data(events_data):
    visit_dates = events_data[[ColNames.TECH_NAME, ColNames.EVENT_DATE]].drop_duplicates()

    #TODO: return the end date to the below line:
    visit_dates['data_end_date'] = visit_dates[ColNames.EVENT_DATE].max()



    # Sort by technician and event_date
    visit_dates = visit_dates.sort_values(by=[ColNames.TECH_NAME, ColNames.EVENT_DATE])

    # Function to calculate business day gaps

    # Apply the function per technician
    vacation_data = find_vacations(visit_dates)

    vacation_data = vacation_data[[ColNames.TECH_NAME,'time_since_vacation', 'vacation_length']]
    return vacation_data


def calc_vacation_score(events_data):
    vacation_data = calc_vacation_data(events_data)
    vacation_data_w_score = score_column(vacation_data,'time_since_vacation')
    return vacation_data_w_score