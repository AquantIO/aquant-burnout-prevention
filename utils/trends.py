import pandas as pd

from utils.function_inputs import DetectSharpChangesWFuncInput
from utils.schema_def import ColNames


def detect_sharp_changes(df, numerical_col, threshold=1.5, lookback_period='30D', output_type='summary'):
    """
    Detects sharp changes in a numerical column by comparing recent values to historical values for each agent.

    Parameters:
    - df: pandas DataFrame containing the data
    - event_agent_col: str, the column name for the categorical grouping (e.g., technician name)
    - event_date_col: str, the column name for the date (e.g., event date)
    - numerical_col: str, the column name for the numerical values to track (e.g., labor duration)
    - threshold: float, z-score threshold for flagging a technician (default is 1.5)
    - lookback_period: str, the time period to consider for detecting recent changes (default is 30 days)
    - output_type: str, type of output ('summary', 'detailed', 'flagged_technicians')

    Returns:
    - Depending on the output_type:
      * 'summary' - Returns a summary DataFrame with technicians and whether they had sharp changes.
      * 'detailed' - Returns a DataFrame with the historical and recent means, std, z-scores, and flags for sharp changes.
      * 'flagged_technicians' - Returns only the technicians that were flagged for sharp changes.
    """
    # Convert event_date_col to datetime

    # Filter recent data within the lookback period
    recent_df = df[df[ColNames.EVENT_DATE] >= (df[ColNames.EVENT_DATE].max() - pd.to_timedelta(lookback_period))]

    # Group original data by technician (agent) and calculate historical statistics
    historical_stats = df.groupby(ColNames.TECH_NAME)[numerical_col].agg(['mean', 'std', 'count']).reset_index()

    # Group recent data by technician and calculate recent statistics
    recent_stats = recent_df.groupby(ColNames.TECH_NAME)[numerical_col].agg(['mean', 'count']).reset_index()
    recent_stats.columns = [ColNames.TECH_NAME, 'recent_mean', 'recent_count']

    # Merge historical and recent statistics
    comparison_df = pd.merge(recent_stats, historical_stats, on=ColNames.TECH_NAME, how='left')

    # Calculate z-scores comparing recent mean against historical mean
    comparison_df['z_score'] = (comparison_df['recent_mean'] - comparison_df['mean']) / comparison_df['std']

    # Flag technicians where the z-score exceeds the threshold
    comparison_df['sharp_change'] = comparison_df['z_score'].abs() > threshold

    # Define output options
    if output_type == 'summary':
        return comparison_df[[ColNames.TECH_NAME, 'sharp_change']]

    elif output_type == 'detailed':
        return comparison_df[[ColNames.TECH_NAME, 'recent_mean', 'mean', 'std', 'z_score', 'sharp_change']]

    elif output_type == 'flagged_technicians':
        return comparison_df[comparison_df['sharp_change']][[ColNames.TECH_NAME, 'recent_mean', 'mean', 'z_score']]

    else:
        raise ValueError(f"Unknown output_type: {output_type}")


import pandas as pd


def detect_sharp_changes_with_function(func_input: DetectSharpChangesWFuncInput):
    """
    Detects sharp changes by applying a user-defined function to a numerical column,
    and comparing the output between recent and historical values for each agent.

    Parameters:
    - df: pandas DataFrame containing the data.
    - numerical_col: str, the column name for the numerical values to track (e.g., labor duration).
    - func: function, a user-defined function to apply to the numerical data (e.g., mean, median).
    - threshold: float, z-score threshold for flagging a technician (default is 1.5).
    - lookback_period: str, the time period to consider for detecting recent changes (default is 30 days).
    - output_type: str, type of output ('summary', 'detailed', 'flagged_technicians').

    Returns:
    - Depending on the output_type:
      * 'summary' - Returns a summary DataFrame with technicians and whether they had sharp changes.
      * 'detailed' - Returns a DataFrame with recent and historical function outputs, z-scores, and flags for sharp changes.
      * 'flagged_technicians' - Returns only the technicians that were flagged for sharp changes.
    """
    # Convert event_date_col to datetime
    func_input.df[ColNames.EVENT_DATE] = pd.to_datetime(func_input.df[ColNames.EVENT_DATE])

    # Filter recent data based on the lookback period
    recent_df = func_input.df[func_input.df[ColNames.EVENT_DATE] >= (func_input.df[ColNames.EVENT_DATE].max() - pd.to_timedelta(func_input.lookback_period))]
    historical_df = func_input.df[func_input.df[ColNames.EVENT_DATE] < (func_input.df[ColNames.EVENT_DATE].max() - pd.to_timedelta(func_input.lookback_period))]
    # Group by technician and apply the function to both historical and recent data
    recent_stats = func_input.func(recent_df)
    historical_stats = func_input.func(historical_df)

    if func_input.eval_col is not None:
        value_col = func_input.eval_col
    else:
        value_col = recent_stats.columns[-2]
    recent_stats = recent_stats[[ColNames.TECH_NAME,value_col]]
    historical_stats = historical_stats[[ColNames.TECH_NAME,value_col]]

    recent_col = f'{value_col}_recent'
    historical_col = f'{value_col}_historical'
    recent_stats = recent_stats.rename(columns={value_col:recent_col})
    historical_stats = historical_stats.rename(columns={value_col:historical_col})


    # Merge historical and recent statistics
    comparison_df = pd.merge(historical_stats, recent_stats, on=ColNames.TECH_NAME, how='left')

    # Calculate z-scores or percentage change (you can modify this based on preference)
    comparison_df['rel_difference'] = (comparison_df[recent_col] - comparison_df[historical_col])/comparison_df[historical_col]
    if func_input.detection_type == 'INCREASE':
        comparison_df['sharp_change'] = comparison_df['rel_difference'] > func_input.threshold
    elif func_input.detection_type == 'DECREASE':
            comparison_df['sharp_change'] = -1 * comparison_df['rel_difference'] > func_input.threshold
    else:
        comparison_df['sharp_change'] = comparison_df['rel_difference'].abs() > func_input.threshold
    # Define output options
    if func_input.output_type == 'summary':
        return comparison_df[[ColNames.TECH_NAME, 'sharp_change']]

    elif func_input.output_type == 'detailed':
        return comparison_df[[ColNames.TECH_NAME, recent_col, historical_col, 'rel_difference', 'sharp_change']]

    elif func_input.output_type == 'flagged_technicians':
        return comparison_df[comparison_df['sharp_change']][[ColNames.TECH_NAME, recent_col, historical_col, 'rel_difference']]

    else:
        raise ValueError(f"Unknown output_type: {func_input.output_type}")

# Example usage:
# result = detect_sharp_changes_with_function(df, 'event_agent_name', 'event_date', 'labor_duration', func=np.mean, threshold=10, lookback_period='60D', output_type='summary')
