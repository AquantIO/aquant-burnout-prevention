from textblob import TextBlob
import pandas as pd
import numpy as np

from utils.preprocessing import prepare_events_data
from utils.schema_def import ColNames


# Function to get sentiment polarity
def get_sentiment(text):
    try:
        blob = TextBlob(text)
        return blob.sentiment.polarity
    except:
        return 0


def get_agent_average_sentiment(events_data):
    events_data['sentiment'] = events_data['freetext'].apply(get_sentiment)
    agent_sentiment = events_data.groupby(ColNames.TECH_NAME)['sentiment'].mean().reset_index()
    agent_sentiment = agent_sentiment.rename(columns={'sentiment': 'average_sentiment'})
    agent_sentiment = agent_sentiment[[ColNames.TECH_NAME, 'average_sentiment']]
    return agent_sentiment


def count_negative_sentiment_rate(events_data):
    ignore_words = {'issue', 'horrific', 'shocking', 'terrible', 'bad', 'brutal', 'errors', 'fault', 'noisy', 'failure', 'damaged', 'defect', 'deformed', 'broken'}

    sentiment_data = events_data.copy()
    def preprocess_text(text):
        words = str(text).split()
        # Remove words in ignore_words from the text
        filtered_words = [word for word in words if word.lower() not in ignore_words]
        return ' '.join(filtered_words)

    # Apply preprocessing to the freetext column
    sentiment_data['filtered_text'] = sentiment_data['freetext'].apply(preprocess_text)

    # Assuming `get_sentiment` returns a sentiment score between -1 and 1
    sentiment_data['sentiment'] = sentiment_data['filtered_text'].apply(get_sentiment)

    # Calculate z-scores for the sentiment column
    sentiment_mean = sentiment_data['sentiment'].mean()
    sentiment_std = sentiment_data['sentiment'].std()
    sentiment_data['sentiment_z'] = (sentiment_data['sentiment'] - sentiment_mean) / sentiment_std

    # Filter using a z-score threshold of -3
    negative_threshold = -5
    sentiment_data['negative_event'] = np.where(sentiment_data['sentiment_z'] <= negative_threshold, 1, 0)
    sentiment_data['all_events'] = 1

    # Count the number of overtly negative events per agent, and all events
    agent_negative_event_rate = sentiment_data.groupby(ColNames.TECH_NAME).agg(
        negative_event_count=('negative_event', 'sum'),
        all_event_count=('all_events', 'sum')
    ).reset_index()
    agent_negative_event_rate['negative_event_rate'] = agent_negative_event_rate['negative_event_count'] / agent_negative_event_rate['all_event_count']
    return agent_negative_event_rate


def negative_sentiment_score(events_data):
    agent_sentiment = count_negative_sentiment_rate(events_data)
    agent_sentiment['negative_event_score'] = agent_sentiment['negative_event_count'] / len(events_data)
    return agent_sentiment



