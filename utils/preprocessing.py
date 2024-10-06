import numpy as np
import pandas as pd

from utils.schema_def import ColNames


def prepare_events_data(events_data):
    events_data = events_data.copy()
    events_data[ColNames.EVENT_DATE] = pd.to_datetime(events_data[ColNames.EVENT_DATE], errors='coerce')
    events_data[ColNames.EVENT_ID] = events_data[ColNames.EVENT_ID].astype(str)

    #filter for event agents with events in the last month
    events_data['agent_last_visit'] = events_data.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('max')
    events_data['agent_days_since_last_visit'] = (events_data[ColNames.EVENT_DATE].max()-events_data['agent_last_visit'])/np.timedelta64(1,'D')
    events_data = events_data[events_data['agent_days_since_last_visit']<=30]



    #define column types
    col_types = {
        ColNames.EVENT_DATE: 'datetime64[ns]',
        ColNames.EVENT_ID: 'str',
        ColNames.TECH_NAME: 'str',
        ColNames.LABOR_DURATION: 'float',
        ColNames.TRAVEL_TIME: 'float',
        ColNames.FREE_TEXT: 'str'
    }
    for col, dtype in col_types.items():
        if col in events_data.columns:
            if col in col_types.keys():
                events_data[col] = events_data[col].astype(dtype)

    return events_data