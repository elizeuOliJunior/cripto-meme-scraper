import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Remove a tentativa de download em tempo de execução e o try-except problemático
# O download do vader_lexicon será feito via setup_nltk.py durante o build do Railway

def analyze_sentiment(text):
    if not isinstance(text, str):
        return {"neg": 0.0, "neu": 0.0, "pos": 0.0, "compound": 0.0}
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)
