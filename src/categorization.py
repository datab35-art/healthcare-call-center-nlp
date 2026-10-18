"""Call reason categorization using TF-IDF and keyword matching."""

import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

CATEGORY_KEYWORDS = {
    "billing": ["bill", "charge", "payment", "premium", "owe", "invoice", "eob", "deductible", "collections"],
    "claims": ["claim", "denied", "denial", "pending", "reprocess", "appeal", "submitted", "status"],
    "prescription": ["prescription", "medication", "pharmacy", "formulary", "copay", "prior authorization", "mail-order", "step therapy"],
    "appointment": ["appointment", "specialist", "referral", "telehealth", "doctor", "provider", "directory", "wellness visit"],
    "general_inquiry": ["benefits", "coverage", "enroll", "member id", "insurance card", "network", "moving", "newborn"],
}


def keyword_categorize(text: str) -> str:
    text_lower = text.lower()
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(1 for kw in keywords if re.search(rf"\b{re.escape(kw)}\b", text_lower))
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "uncategorized"


def build_tfidf_features(corpus: pd.Series, max_features: int = 500) -> tuple:
    vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=(1, 2), stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return tfidf_matrix, vectorizer


def add_predicted_category(df: pd.DataFrame) -> pd.DataFrame:
    df["predicted_category"] = df["transcript"].apply(keyword_categorize)
    return df
