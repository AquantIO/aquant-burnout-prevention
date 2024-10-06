from causes.time_off import calc_vacation_score
from causes.travel_time import calc_agent_travel_time_score
from causes.workload import calc_agent_caseload_score, calc_agent_labor_duration_score
from utils.schema_def import ColNames

def get_metric_weights():
    return {
        'caseload_score': 6.0,
        'labor_duration_score': 0,
        'time_since_vacation_score': 2.0,
        'travel_time_score': 3.0
    }




def calculate_burnout_index_causes(events_data):
    # Initialize the main dataframe with only unique technician names
    agent_scores = events_data[[ColNames.TECH_NAME]].drop_duplicates().reset_index(drop=True)

    # List of functions to execute, along with their expected score column
    scoring_functions = [
        (calc_agent_caseload_score, 'caseload_score'),
        (calc_agent_labor_duration_score, 'labor_duration_score'),
        (calc_vacation_score, 'time_since_vacation_score'),
        (calc_agent_travel_time_score, 'travel_p_day_avg_score')
    ]

    # Track successful score columns
    score_columns = []

    # Run scoring functions and merge results
    for func, score_column in scoring_functions:
        result_df = func(events_data)
        if len(result_df) > 0:
            # Merge only if the function was successful
            agent_scores = agent_scores.merge(result_df, on=ColNames.TECH_NAME, how='left')
            # Add the relevant score column if it ends with '_score'
            if score_column.endswith('_score'):
                score_columns.append(score_column)

    # Calculate the final weighted score using the relevant score columns
    weights = get_metric_weights()
    agent_scores['burnout_index_causes'] = agent_scores[score_columns].apply(
        lambda row: sum(row[col] * weights.get(col, 0) for col in score_columns if col in weights),
        axis=1
    )

    #normalise to a scale of 0-10
    max_possible_score = sum([weights[x] for x in weights.keys() if x in score_columns])
    agent_scores['burnout_index_causes'] = 10 * agent_scores['burnout_index_causes'] / max_possible_score


    return agent_scores

