from utils.schema_def import ColNames
import pandas as pd

from utils.wrappers import safe_execution


@safe_execution(expected_columns=[ColNames.TECH_NAME])
def find_outlier_labor_durations(events_data_in, z_threshold=2.0):
    # Copy relevant columns
    agent_labor_durations = events_data_in[[ColNames.TECH_NAME, ColNames.EVENT_DATE, ColNames.LABOR_DURATION, ColNames.PRODUCT_TYPE]].copy()

    # Calculate the mean and standard deviation of labor duration for each technician and product type
    agent_labor_durations['mean_labor_duration'] = agent_labor_durations.groupby(
        [ColNames.TECH_NAME, ColNames.PRODUCT_TYPE]
    )[ColNames.LABOR_DURATION].transform('mean')

    agent_labor_durations['std_labor_duration'] = agent_labor_durations.groupby(
        [ColNames.TECH_NAME, ColNames.PRODUCT_TYPE]
    )[ColNames.LABOR_DURATION].transform('std')

    # Calculate the z-score for each labor duration
    agent_labor_durations['z_score'] = (agent_labor_durations[ColNames.LABOR_DURATION] - agent_labor_durations['mean_labor_duration']) / agent_labor_durations['std_labor_duration']

    # Identify events that are too short or too long
    agent_labor_durations['all_events'] = 1
    agent_labor_durations['is_too_short'] = agent_labor_durations['z_score'] < -z_threshold
    agent_labor_durations['is_too_long'] = agent_labor_durations['z_score'] > z_threshold


    return agent_labor_durations


def outlier_duration_score(events_data):
    outlier_agent_labor_durations = find_outlier_labor_durations(events_data)
    # Calculate the number of too short and too long events for each technician
    outlier_labor_duration_score = outlier_agent_labor_durations.groupby(ColNames.TECH_NAME).agg(
        total_events=('all_events', 'sum'),
        num_too_short=('is_too_short', 'sum'),
        num_too_long=('is_too_long', 'sum')
    ).reset_index()

    # Merge the summary back to the main dataframe
    outlier_labor_duration_score['outlier_labor_duration_score'] = (outlier_labor_duration_score['num_too_short'] + outlier_labor_duration_score['num_too_long'])/outlier_labor_duration_score['total_events']
    outlier_labor_duration_score = outlier_labor_duration_score[[ColNames.TECH_NAME, 'outlier_labor_duration_score']]
    return outlier_labor_duration_score
