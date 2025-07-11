import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Garante que o vader_lexicon seja baixado se não estiver presente
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    print("vader_lexicon não encontrado. Tentando baixar...")
    # Tenta baixar o léxico. Se falhar, a exceção será propagada.
    nltk.download("vader_lexicon", quiet=True) # quiet=True para evitar output excessivo

def analyze_sentiment(text):
    if not isinstance(text, str):
        return {"neg": 0.0, "neu": 0.0, "pos": 0.0, "compound": 0.0}
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)
