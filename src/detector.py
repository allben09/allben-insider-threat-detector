"""
src/detector.py
Insider Threat Detector - ML Ensemble

Combines Isolation Forest and One-Class SVM for behavioural anomaly
detection. Produces risk scores and ranked threat lists.

Author: Allben Rakgoale
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from features import MODEL_FEATURES


class InsiderThreatDetector:
    """
    Ensemble anomaly detector for insider threats.

    Combines:
      - Isolation Forest (tree-based outlier detection)
      - One-Class SVM (boundary-based anomaly detection)

    Final risk score = weighted average of both models' normalised scores.
    """

    def __init__(self, contamination: float = 0.1):
        self.contamination = contamination
        self.scaler = StandardScaler()

        self.iso_forest = IsolationForest(
            n_estimators=200,
            contamination=contamination,
            random_state=42,
            n_jobs=-1,
        )

        self.ocsvm = OneClassSVM(
            kernel="rbf",
            gamma="auto",
            nu=contamination,
        )

        self.feature_columns = MODEL_FEATURES

    # -----------------------------------------------------
    # Training
    # -----------------------------------------------------
    def fit(self, features: pd.DataFrame) -> "InsiderThreatDetector":
        """Train the ensemble on the engineered feature set."""
        X = features[self.feature_columns].fillna(0).values
        X_scaled = self.scaler.fit_transform(X)

        self.iso_forest.fit(X_scaled)
        self.ocsvm.fit(X_scaled)

        return self

    # -----------------------------------------------------
    # Scoring
    # -----------------------------------------------------
    def score(self, features: pd.DataFrame) -> pd.DataFrame:
        """
        Return a DataFrame with risk scores and predictions.

        Adds:
          - iso_score: normalised Isolation Forest score (0-1)
          - svm_score: normalised One-Class SVM score (0-1)
          - risk_score: ensemble score (0-1)
          - predicted_threat: 1 if risk_score >= threshold
        """
        X = features[self.feature_columns].fillna(0).values
        X_scaled = self.scaler.transform(X)

        # Isolation Forest returns negative scores (lower = more anomalous)
        iso_raw = -self.iso_forest.score_samples(X_scaled)
        iso_score = self._normalise(iso_raw)

        # One-Class SVM decision function (lower = more anomalous)
        svm_raw = -self.ocsvm.decision_function(X_scaled)
        svm_score = self._normalise(svm_raw)

        # Ensemble (weighted average)
        risk_score = (0.6 * iso_score) + (0.4 * svm_score)

        results = features.copy()
        results["iso_score"] = iso_score
        results["svm_score"] = svm_score
        results["risk_score"] = risk_score

        threshold = np.percentile(risk_score, (1 - self.contamination) * 100)
        results["predicted_threat"] = (risk_score >= threshold).astype(int)

        return results.sort_values("risk_score", ascending=False)

    @staticmethod
    def _normalise(arr: np.ndarray) -> np.ndarray:
        """Min-max normalisation to 0-1 range."""
        mn, mx = arr.min(), arr.max()
        if mx - mn < 1e-9:
            return np.zeros_like(arr)
        return (arr - mn) / (mx - mn)

    # -----------------------------------------------------
    # Report
    # -----------------------------------------------------
    def evaluate(self, scored: pd.DataFrame) -> dict:
        """Compare predictions against ground truth (if available)."""
        if "is_threat" not in scored.columns:
            return {}

        from sklearn.metrics import (
            precision_score, recall_score, f1_score,
        )

        y_true = scored["is_threat"]
        y_pred = scored["predicted_threat"]

        return {
            "precision": round(precision_score(y_true, y_pred, zero_division=0), 3),
            "recall": round(recall_score(y_true, y_pred, zero_division=0), 3),
            "f1": round(f1_score(y_true, y_pred, zero_division=0), 3),
        }


def run_pipeline(activity_df: pd.DataFrame, contamination: float = 0.1) -> pd.DataFrame:
    """
    Full pipeline: engineer features → train ensemble → return scored users.
    """
    from features import engineer_features

    features = engineer_features(activity_df)

    detector = InsiderThreatDetector(contamination=contamination)
    detector.fit(features)

    scored = detector.score(features)
    return scored


if __name__ == "__main__":
    from data_generator import generate_dataset

    print("🔍 Generating data...")
    df = generate_dataset(n_employees=50, threat_ratio=0.1)

    print("⚙️  Running detector pipeline...")
    scored = run_pipeline(df)

    print("\n🚨 Top 10 Suspicious Users:")
    print(scored[[
        "user_id", "name", "department", "risk_score", "predicted_threat"
    ]].head(10).to_string(index=False))

    detector = InsiderThreatDetector()
    detector.fit(scored)
    metrics = detector.evaluate(scored)
    print(f"\n📊 Detection Metrics: {metrics}")
