"""
FD-XIDS Production Training Pipeline

Requirements implemented:
- Load raw CICIDS2017 CSV from `backend/data/raw/cicids2017.csv`
- Clean NaNs/infs, strip whitespace from column names
- Convert labels to binary (BENIGN -> 0, attacks -> 1) with target `Label`
- Remove highly correlated features (corr > 0.9)
- Scale features with `StandardScaler`
- Train/Test split (80/20 stratified, random_state=42)
- Train LogisticRegression baseline and RandomForest main model
- Evaluate Accuracy, Precision, Recall, F1, Confusion Matrix, ROC-AUC
- Compare models and highlight best by F1
- Extract RandomForest feature importances, save top 15 and CSV
- Generate SHAP TreeExplainer summary and bar plots
- Save models to `backend/models/saved_models/`

Usage:
    python backend/models/train_pipeline_fd_xids.py

This script is modular and intended to be run from the project root.
"""

import os
from typing import Tuple, List

import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import shap

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    classification_report,
)


RAW_DATA_PATH = os.path.join("..", "data", "raw", "cicids2017.csv")
SAVE_DIR_MODELS = os.path.join(os.path.dirname(__file__), "saved_models")
FI_CSV_PATH = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "results", "metrics", "feature_importance.csv")
SHAP_PLOTS_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "results", "explanations")


def load_and_clean(path: str) -> pd.DataFrame:
    """Load CSV, drop NaN/inf rows, strip column whitespace, and normalize label.

    Feature-driven rationale: ensure clean, deterministic inputs so feature
    importance reflects real signal, not artifacts from bad rows or noisy names.
    """
    if not os.path.isabs(path):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))

    if not os.path.exists(path):
        raise FileNotFoundError(f"Raw dataset not found at {path}")

    df = pd.read_csv(path)

    # Strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]

    # Drop rows with NaN or infinite values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    # Normalize label column: user requested 'Label' as target name
    if "Label" not in df.columns and "label" in df.columns:
        df.rename(columns={"label": "Label"}, inplace=True)

    if "Label" not in df.columns:
        raise ValueError("Expected a target column named 'Label' in raw CSV")

    # Map labels: BENIGN -> 0, everything else -> 1
    df["Label"] = df["Label"].astype(str).str.strip()
    df["Label"] = df["Label"].apply(lambda x: 0 if x.upper() == "BENIGN" else 1)

    return df


def remove_correlated_features(X: pd.DataFrame, threshold: float = 0.9) -> Tuple[pd.DataFrame, List[str]]:
    """Remove highly correlated features above `threshold`.

    Keeps the first occurrence and drops later correlated columns. Returns the
    reduced DataFrame and a list of dropped feature names.

    FD-XIDS reason: removing redundant features focuses importance on distinct
    signals (feature-driven principle) and reduces multicollinearity.
    """
    corr = X.corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))

    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    X_reduced = X.drop(columns=to_drop)
    return X_reduced, to_drop


def preprocess_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, StandardScaler]:
    """Separate features and label, remove correlated features, and scale.

    Returns scaled training-ready DataFrame, label Series, and the fitted scaler.
    """
    X = df.drop(columns=["Label"]).copy()
    y = df["Label"].copy()

    X_reduced, dropped = remove_correlated_features(X, threshold=0.9)
    if dropped:
        print(f"Dropped {len(dropped)} highly correlated features:")
        print(dropped)

    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X_reduced), columns=X_reduced.columns)

    return X_scaled, y, scaler


def train_and_evaluate(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> Tuple[dict, dict, pd.DataFrame]:
    """Train LogisticRegression baseline and RandomForest, evaluate metrics,
    and return model dict, metrics dict, and comparison DataFrame.
    """
    models = {}
    metrics = {}

    # Model 1: Logistic Regression (baseline)
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)
    models["LogisticRegression"] = lr

    # Model 2: Random Forest (main model)
    rf = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    models["RandomForest"] = rf

    def _eval(model, X_t, y_t):
        y_pred = model.predict(X_t)
        y_proba = None
        try:
            y_proba = model.predict_proba(X_t)[:, 1]
        except Exception:
            pass

        result = {
            "accuracy": accuracy_score(y_t, y_pred),
            "precision": precision_score(y_t, y_pred, zero_division=0),
            "recall": recall_score(y_t, y_pred, zero_division=0),
            "f1": f1_score(y_t, y_pred, zero_division=0),
            "confusion_matrix": confusion_matrix(y_t, y_pred),
        }
        if y_proba is not None:
            try:
                result["roc_auc"] = roc_auc_score(y_t, y_proba)
            except Exception:
                result["roc_auc"] = float("nan")
        else:
            result["roc_auc"] = float("nan")

        return result

    for name, model in models.items():
        print(f"\nEvaluating {name}...")
        m = _eval(model, X_test, y_test)
        metrics[name] = m
        print(f"Accuracy: {m['accuracy']:.4f}, Precision: {m['precision']:.4f}, Recall: {m['recall']:.4f}, F1: {m['f1']:.4f}, ROC-AUC: {m['roc_auc'] if not pd.isna(m['roc_auc']) else 'N/A'}")
        print("Confusion Matrix:")
        print(m["confusion_matrix"])

    # Comparison DataFrame
    comp = pd.DataFrame.from_dict({k: {"accuracy": v["accuracy"], "precision": v["precision"], "recall": v["recall"], "f1": v["f1"], "roc_auc": v.get("roc_auc", np.nan)} for k, v in metrics.items()}, orient="index")

    # Highlight best by F1
    best_model = comp["f1"].idxmax()
    comp["best_by_f1"] = False
    comp.loc[best_model, "best_by_f1"] = True

    print("\nModel comparison:")
    print(comp)

    return models, metrics, comp


def save_feature_importance(rf_model: RandomForestClassifier, feature_names: List[str], top_n: int = 15):
    """Extract and save feature importances for feature-driven analysis."""
    importances = rf_model.feature_importances_
    fi = pd.DataFrame({"feature": feature_names, "importance": importances})
    fi_sorted = fi.sort_values(by="importance", ascending=False)

    os.makedirs(os.path.dirname(FI_CSV_PATH), exist_ok=True)
    fi_sorted.to_csv(FI_CSV_PATH, index=False)
    print(f"Saved feature importances to {FI_CSV_PATH}")

    print("\nTop {n} features:".format(n=top_n))
    print(fi_sorted.head(top_n).to_string(index=False))

    return fi_sorted


def generate_shap_plots(rf_model: RandomForestClassifier, X: pd.DataFrame):
    """Generate SHAP summary and bar plots and save them to disk.

    Uses a sample if dataset is large to keep plotting time reasonable.
    """
    os.makedirs(SHAP_PLOTS_DIR, exist_ok=True)

    n_samples = min(1000, len(X))
    X_sample = X.sample(n=n_samples, random_state=42)

    # Create TreeExplainer and compute SHAP values
    explainer = shap.TreeExplainer(rf_model)
    shap_values = explainer.shap_values(X_sample)

    # shap_values might be list for multiclass; for binary, take index 1
    if isinstance(shap_values, list):
        # choose the explanation for positive class
        shap_vals = shap_values[1]
    else:
        shap_vals = shap_values

    # Summary plot
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_vals, X_sample, show=False)
    summary_path = os.path.join(SHAP_PLOTS_DIR, "shap_summary.png")
    plt.savefig(summary_path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Saved SHAP summary plot to {summary_path}")

    # Bar plot (mean absolute value)
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_vals, X_sample, plot_type="bar", show=False)
    bar_path = os.path.join(SHAP_PLOTS_DIR, "shap_bar.png")
    plt.savefig(bar_path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Saved SHAP bar plot to {bar_path}")


def save_models(models: dict):
    os.makedirs(SAVE_DIR_MODELS, exist_ok=True)
    # logistic
    if "LogisticRegression" in models:
        p = os.path.join(SAVE_DIR_MODELS, "logistic_cicids.pkl")
        joblib.dump(models["LogisticRegression"], p)
        print(f"Saved LogisticRegression to {p}")

    # random forest
    if "RandomForest" in models:
        p = os.path.join(SAVE_DIR_MODELS, "fd_xids_rf_cicids.pkl")
        joblib.dump(models["RandomForest"], p)
        print(f"Saved RandomForest to {p}")


def main():
    print("Starting FD-XIDS training pipeline...")
    raw_path = os.path.join(os.path.dirname(__file__), RAW_DATA_PATH)
    df = load_and_clean(raw_path)

    X, y, scaler = preprocess_features(df)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    models, metrics, comp = train_and_evaluate(X_train, X_test, y_train, y_test)

    # Feature-driven analysis: Random Forest importances
    rf_model = models.get("RandomForest")
    fi_sorted = save_feature_importance(rf_model, list(X.columns), top_n=15)

    # SHAP explainability
    try:
        generate_shap_plots(rf_model, X_train)
    except Exception as e:
        print(f"SHAP plotting failed: {e}")

    # Save models
    save_models(models)

    print("FD-XIDS training pipeline completed.")


if __name__ == "__main__":
    main()
