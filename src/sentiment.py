"""Sentiment analysis on call transcripts using VADER."""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon", quiet=True)

_analyzer = SentimentIntensityAnalyzer()


def get_sentiment_scores(text: str) -> dict:
    return _analyzer.polarity_scores(text)


def classify_sentiment(compound_score: float) -> str:
    if compound_score >= 0.05:
        return "positive"
    if compound_score <= -0.05:
        return "negative"
    return "neutral"


def add_sentiment_columns(df):
    scores = df["transcript"].apply(get_sentiment_scores)
    df["sentiment_compound"] = scores.apply(lambda s: s["compound"])
    df["sentiment_pos"] = scores.apply(lambda s: s["pos"])
    df["sentiment_neg"] = scores.apply(lambda s: s["neg"])
    df["sentiment_class"] = df["sentiment_compound"].apply(classify_sentiment)
    return df
