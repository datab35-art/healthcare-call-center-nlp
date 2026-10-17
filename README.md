# Healthcare Call Center NLP Analytics

End-to-end NLP pipeline that analyzes healthcare call center transcripts to surface actionable insights — complaint categorization, sentiment analysis, friction-point detection, and repeat-caller patterns.

## Business Problem

Healthcare call centers handle thousands of member interactions daily. Understanding **why** members call, **what** frustrates them, and **who** calls back repeatedly is critical for improving member experience and reducing operational costs.

## Approach

1. **Synthetic Data Generation** — realistic call transcripts covering billing, claims, prescription, appointment, and general inquiry topics
2. **Text Preprocessing** — cleaning, tokenization, stopword removal, lemmatization
3. **Sentiment Analysis** — VADER-based polarity scoring per transcript
4. **Topic / Complaint Categorization** — TF-IDF + keyword-based classification of call reasons
5. **Friction Point Detection** — identifying escalation language, long hold references, transfer mentions
6. **Repeat Caller Analysis** — cohort analysis of members with multiple contacts
7. **Insights Dashboard** — summary visualizations of KPIs (FCR, sentiment trends, top complaint categories)

## Key Findings

| Metric | Value |
|--------|-------|
| First Contact Resolution (FCR) | ~62% |
| Top Complaint Category | Billing / Claims |
| Avg. Sentiment (frustrated callers) | -0.45 |
| Repeat Caller Rate | ~28% |

## Tech Stack

- **Python 3.11** — pandas, scikit-learn, nltk, matplotlib, seaborn
- **NLP** — TF-IDF vectorization, VADER sentiment, regex-based entity extraction
- **Visualization** — matplotlib, seaborn

## Project Structure

```
├── data/
│   └── synthetic_call_transcripts.csv
├── notebooks/
│   └── call_center_nlp_analysis.ipynb
├── src/
│   ├── generate_data.py
│   ├── preprocessing.py
│   ├── sentiment.py
│   ├── categorization.py
│   ├── friction.py
│   └── repeat_callers.py
├── requirements.txt
└── README.md
```

## How to Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py          # generate synthetic transcripts
jupyter notebook notebooks/          # explore the analysis
```

## Skills Demonstrated

- Natural Language Processing (NLP) & text analytics
- Voice / interaction analytics methodology
- Healthcare member experience domain
- Data storytelling & executive-ready visualizations
