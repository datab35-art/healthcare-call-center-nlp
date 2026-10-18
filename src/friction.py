"""Friction point detection in call transcripts."""

import re

FRICTION_PATTERNS = {
    "long_hold": [r"on hold for (?:over )?\d+", r"waiting (?:for )?\d+ minutes", r"hold for (?:over )?(?:an )?hour"],
    "multiple_transfers": [r"transferred (?:\w+ )?times", r"bounced around", r"sent (?:me )?in circles"],
    "repeat_contact": [r"(?:called|calling) (?:\w+ )?times", r"third|fourth|fifth call", r"called .* about (?:the )?same"],
    "escalation_request": [r"speak to (?:a )?(?:supervisor|manager)", r"(?:file|filing) a (?:formal )?complaint", r"escalat"],
    "disconnection": [r"disconnected", r"hung up on", r"call (?:was )?dropped"],
    "system_issues": [r"automated system", r"sent (?:me )?in circles", r"website .* (?:not |doesn't )work"],
    "repeated_explanation": [r"already explained", r"told (?:the )?last (?:representative|agent|person)", r"explain(?:ed)? .* again"],
}


def detect_friction_points(text: str) -> dict[str, bool]:
    results = {}
    for friction_type, patterns in FRICTION_PATTERNS.items():
        results[friction_type] = any(re.search(p, text, re.IGNORECASE) for p in patterns)
    return results


def add_friction_columns(df):
    friction_df = df["transcript"].apply(detect_friction_points).apply(lambda d: {f"friction_{k}": v for k, v in d.items()})
    import pandas as pd
    friction_cols = pd.DataFrame(friction_df.tolist(), index=df.index)
    df = pd.concat([df, friction_cols], axis=1)
    df["friction_count"] = friction_cols.sum(axis=1)
    df["has_friction"] = df["friction_count"] > 0
    return df
