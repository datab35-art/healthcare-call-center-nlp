"""Repeat caller analysis and cohort metrics."""

import pandas as pd


def add_repeat_caller_flags(df: pd.DataFrame) -> pd.DataFrame:
    call_counts = df.groupby("member_id")["call_id"].transform("count")
    df["total_calls"] = call_counts
    df["is_repeat_caller"] = call_counts > 1
    return df


def repeat_caller_summary(df: pd.DataFrame) -> pd.DataFrame:
    repeat = df[df["is_repeat_caller"]].copy()
    summary = (
        repeat.groupby("member_id")
        .agg(
            total_calls=("call_id", "count"),
            categories_contacted=("category", "nunique"),
            primary_category=("category", lambda x: x.mode().iloc[0]),
            avg_sentiment=("sentiment_compound", "mean"),
            resolution_rate=("resolved", "mean"),
            avg_duration=("duration_minutes", "mean"),
            friction_incidents=("has_friction", "sum"),
            date_first_call=("call_date", "min"),
            date_last_call=("call_date", "max"),
        )
        .sort_values("total_calls", ascending=False)
        .reset_index()
    )
    return summary


def compute_fcr(df: pd.DataFrame) -> float:
    single_call_members = df.groupby("member_id").filter(lambda g: len(g) == 1)
    resolved_first = single_call_members["resolved"].mean()
    return resolved_first
