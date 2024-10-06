import functools
import logging
import pandas as pd
# Set up basic logging
logging.basicConfig(level=logging.INFO)

def safe_execution(expected_columns):
    """A decorator to catch exceptions and return a default dataframe with specified columns if an error occurs."""
    def decorator_function(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"Function '{func.__name__}' failed with error: {e}")
                # Return an empty dataframe with the expected columns
                return pd.DataFrame(columns=expected_columns)
        return wrapper
    return decorator_function
