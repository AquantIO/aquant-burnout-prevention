from causes.time_off import calc_vacation_score
from causes.travel_time import calc_agent_travel_time_score
from causes.workload import calc_agent_labor_duration_score
from symptoms.outlier_labor_duration import find_outlier_labor_durations, outlier_duration_score
from symptoms.sentiment_analysis.freetext_sentiment import negative_sentiment_score
from symptoms.sick_leave import count_sick_days
from utils.schema_def import ColNames

def get_symptom_weights():
    return {
        'sick_leave_score': 2,
        'outlier_labor_duration_score': 20.2,
        'negative_event_score': 5.5
    }


def calculate_burnout_index_symptoms(events_data):
    # Initialize the main dataframe with only unique technician names
    agent_symptom_scores = events_data[[ColNames.TECH_NAME]].drop_duplicates().reset_index(drop=True)

    # List of functions to execute, along with their expected score column
    scoring_functions = [
        (count_sick_days, 'sick_leave_score'),
        (outlier_duration_score, 'outlier_labor_duration_score'),
        (negative_sentiment_score, 'negative_event_score')
    ]

    # Track successful score columns
    score_columns = []

    # Run scoring functions and merge results
    for func, score_column in scoring_functions:
        result_df = func(events_data)
        if len(result_df) > 0:
            # Merge only if the function was successful
            agent_symptom_scores = agent_symptom_scores.merge(result_df, on=ColNames.TECH_NAME, how='left')
            # Add the relevant score column if it ends with '_score'
            if score_column.endswith('_score'):
                score_columns.append(score_column)

    # Calculate the final weighted score using the relevant score columns
    weights = get_symptom_weights()
    agent_symptom_scores['burnout_index_symptoms'] = agent_symptom_scores[score_columns].apply(
        lambda row: sum(row[col] * weights.get(col, 0) for col in score_columns if col in weights),
        axis=1
    )

    #normalise to a scale of 0-10
    max_possible_score = sum([weights[x] for x in weights.keys() if x in score_columns])
    agent_symptom_scores['burnout_index_symptoms'] = 10 * agent_symptom_scores['burnout_index_symptoms'] / max_possible_score


    return agent_symptom_scores

