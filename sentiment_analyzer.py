import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except nltk.downloader.DownloadError:
    nltk.download("vader_lexicon")

def analyze_sentiment(text):
    if not isinstance(text, str):
        return {"neg": 0.0, "neu": 0.0, "pos": 0.0, "compound": 0.0}
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)