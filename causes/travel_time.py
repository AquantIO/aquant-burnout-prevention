from utils.schema_def import ColNames
from utils.scoring import score_column
import pandas as pd

from utils.wrappers import safe_execution


def calc_agent_travel_time(events_data_in):
    agent_travel_times = events_data_in[[ColNames.TECH_NAME,ColNames.EVENT_DATE,ColNames.TRAVEL_TIME]].copy()
    agent_travel_times = agent_travel_times.groupby(ColNames.TECH_NAME).agg(
        total_travel_time=pd.NamedAgg(column=ColNames.TRAVEL_TIME, aggfunc='sum'),
        total_workdays=pd.NamedAgg(column=ColNames.EVENT_DATE, aggfunc='nunique')).reset_index()
    agent_travel_times['travel_p_day_avg'] = agent_travel_times['total_travel_time']/agent_travel_times['total_workdays']
    return agent_travel_times

@safe_execution(expected_columns=[ColNames.TECH_NAME])
def calc_agent_travel_time_score(events_data_in):
    agent_workload = calc_agent_travel_time(events_data_in)
    agent_workload_w_score = score_column(agent_workload,'travel_p_day_avg')
    return agent_workload_w_score

