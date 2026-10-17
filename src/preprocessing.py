"""Text preprocessing utilities for call transcripts."""

import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

_lemmatizer = WordNetLemmatizer()
_stop_words = set(stopwords.words("english"))


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\$\d+", " dollar_amount ", text)
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_and_lemmatize(text: str) -> list[str]:
    tokens = word_tokenize(clean_text(text))
    return [_lemmatizer.lemmatize(t) for t in tokens if t not in _stop_words and len(t) > 2]


def preprocess_column(series):
    return series.apply(lambda t: " ".join(tokenize_and_lemmatize(t)))
