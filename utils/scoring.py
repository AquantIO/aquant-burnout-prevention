import pandas as pd
import numpy as np
import scipy.stats as stats




def score_column(df, column_name, inverse=False, z_threshold=3, handle_outliers='cap'):
    # Create a copy of the dataframe to avoid modifying the original directly
    df_copy = df.copy()

    # Step 1: Outlier Detection using Z-Score
    z_scores = np.abs(stats.zscore(df_copy[column_name]))
    df_copy['z_score'] = z_scores
    df_copy[column_name + "_outlier"] = z_scores > z_threshold

    temp_col_name = column_name + "_temp"
    # Step 2: Handle Outliers
    if handle_outliers == 'remove':
        df_copy = df_copy[df_copy[column_name + "_outlier"] == False]
    elif handle_outliers == 'cap':
        lower_bound = df_copy[column_name].quantile(0.01)
        upper_bound = df_copy[column_name].quantile(0.99)
        df_copy[temp_col_name] = np.clip(df_copy[column_name], lower_bound, upper_bound)
    elif handle_outliers == 'impute':
        median_value = df_copy[column_name].median()
        # df_copy.loc[df_copy[column_name + "_outlier"] == True, temp_col_name] = median_value
        df_copy[temp_col_name] = np.where(df_copy[column_name + "_outlier"], median_value, df_copy[column_name])
    elif handle_outliers == 'fixed':
        df_copy.loc[df_copy[column_name + "_outlier"] == True, column_name + "_score"] = 0  # Or 1
        temp_col_name = column_name

    # Step 3: Min-Max Normalization (after handling outliers)
    min_val = df_copy[temp_col_name].min()
    max_val = df_copy[temp_col_name].max()

    if min_val == max_val:
        df_copy[column_name + "_score"] = 0.5  # Assign middle score if no variation
    else:
        df_copy[column_name + "_score"] = (df_copy[temp_col_name] - min_val) / (max_val - min_val)

    # Step 4: Inverse Score if required
    if inverse:
        df_copy[column_name + "_score"] = 1 - df_copy[column_name + "_score"]

    # Step 5: Remove temporary columns to keep the original column intact
    df_copy = df_copy.drop(columns=[column_name + "_outlier",'z_score', temp_col_name])

    return df_copy

