import pandas as pd

from utils.schema_def import ColNames
from utils.wrappers import safe_execution


@safe_execution(expected_columns=[ColNames.TECH_NAME])
def count_sick_days(events_data):
    if 'is_sick_leave' not in events_data.columns:
        raise ValueError("Column 'is_sick_leave' not found in events_data")
    # Assuming `events_data` has 'agent_name', 'event_date', and 'is_sick_leave' columns
    # Filter for sick leave events only
    sick_leave_data = events_data[events_data['is_sick_leave'] == True].copy()

    # Convert 'event_date' to datetime if not already
    sick_leave_data[ColNames.EVENT_DATE] = pd.to_datetime(sick_leave_data[ColNames.EVENT_DATE])

    # Filter out weekends (weekday() returns 0 for Monday and 6 for Sunday)
    sick_leave_data = sick_leave_data[sick_leave_data[ColNames.EVENT_DATE].dt.weekday < 5]

    # Count the number of sick days per technician
    total_sick_days = sick_leave_data.groupby(ColNames.TECH_NAME).size().reset_index(name='total_sick_days')

    return total_sick_days