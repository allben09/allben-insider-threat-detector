"""
src/features.py
Insider Threat Detector - Feature Engineering

Aggregates raw activity logs into per-user behavioural features
for anomaly detection.

Author: Allben Rakgoale
"""

import pandas as pd
import numpy as np


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate per-user features from raw activity logs.

    Returns a DataFrame with one row per user, containing behavioural
    statistics that the ML model will use to detect anomalies.
    """
    grouped = df.groupby("user_id")

    features = pd.DataFrame({
        # Identity
        "name": grouped["name"].first(),
        "department": grouped["department"].first(),

        # Volume metrics
        "total_data_mb": grouped["data_transferred_mb"].sum(),
        "avg_data_mb": grouped["data_transferred_mb"].mean(),
        "max_data_mb": grouped["data_transferred_mb"].max(),

        # Session metrics
        "avg_session_hours": grouped["session_hours"].mean(),
        "max_session_hours": grouped["session_hours"].max(),

        # Login time anomalies
        "min_login_hour": grouped["login_hour"].min(),
        "avg_login_hour": grouped["login_hour"].mean(),
        "std_login_hour": grouped["login_hour"].std().fillna(0),

        # File access
        "total_files": grouped["files_accessed"].sum(),
        "avg_files": grouped["files_accessed"].mean(),
        "max_files": grouped["files_accessed"].max(),

        # Sensitive access
        "total_sensitive": grouped["sensitive_access"].sum(),
        "avg_sensitive": grouped["sensitive_access"].mean(),
        "max_sensitive": grouped["sensitive_access"].max(),

        # Security events
        "total_failed_logins": grouped["failed_logins"].sum(),
        "avg_failed_logins": grouped["failed_logins"].mean(),

        # USB usage
        "total_usb_events": grouped["usb_events"].sum(),
        "days_with_usb": grouped["usb_events"].apply(lambda x: (x > 0).sum()),

        # Activity volume
        "days_active": grouped["date"].count(),

        # Ground truth (for evaluation)
        "is_threat": grouped["is_threat"].max().astype(int),
    }).reset_index()

    # Derived ratios
    features["sensitive_ratio"] = (
        features["total_sensitive"] / features["total_files"].replace(0, 1)
    )
    features["data_per_day"] = (
        features["total_data_mb"] / features["days_active"].replace(0, 1)
    )
    features["files_per_day"] = (
        features["total_files"] / features["days_active"].replace(0, 1)
    )
    features["usb_per_day"] = (
        features["total_usb_events"] / features["days_active"].replace(0, 1)
    )

    return features


# Features used by the ML model (numeric only)
MODEL_FEATURES = [
    "total_data_mb",
    "avg_data_mb",
    "max_data_mb",
    "avg_session_hours",
    "max_session_hours",
    "min_login_hour",
    "std_login_hour",
    "total_files",
    "max_files",
    "total_sensitive",
    "max_sensitive",
    "total_failed_logins",
    "total_usb_events",
    "days_with_usb",
    "days_active",
    "sensitive_ratio",
    "data_per_day",
    "files_per_day",
    "usb_per_day",
]
