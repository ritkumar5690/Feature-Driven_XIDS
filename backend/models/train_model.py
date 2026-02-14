"""
FD-XIDS Training Script

This script trains a Random Forest classifier on the processed FD-XIDS dataset
located at `backend/data/processed/train_processed.csv` by default. It prints
evaluation metrics, extracts feature importances, and saves the trained model
to `backend/models/saved_models/fd_xids_model.pkl`.

Usage:
    python backend/models/train_model.py --data backend/data/processed/train_processed.csv
    python backend/models/train_model.py --tune  # enable grid search tuning
"""

import os
import argparse
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)


def train_fd_xids_model(
    data_path: str,
    save_model_path: str,
    tune: bool = False,
    param_grid: dict | None = None,
    random_state: int = 42,
):
    print(f"Loading processed dataset from {data_path}...")
    df = pd.read_csv(data_path)

    if "label" not in df.columns:
        raise ValueError("Expected a 'label' column in processed dataset")

    X = df.drop("label", axis=1)
    y = df["label"]

    print("Splitting dataset (train/test = 80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )

    if tune:
        print("Running GridSearchCV for hyperparameter tuning...")
        if param_grid is None:
            param_grid = {
                "n_estimators": [100, 200],
                "max_depth": [10, 15, None]
            }

        grid = GridSearchCV(
            RandomForestClassifier(random_state=random_state, n_jobs=-1),
            param_grid,
            cv=3,
            scoring="f1",
            n_jobs=-1,
            verbose=1,
        )

        grid.fit(X_train, y_train)
        model = grid.best_estimator_
        print(f"Best params: {grid.best_params_}")
    else:
        print("Training Random Forest (baseline) with default hyperparameters...")
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            random_state=random_state,
            n_jobs=-1
        )
        model.fit(X_train, y_train)

    print("Evaluating model on test set...")
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1 Score: {f1:.4f}")

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    try:
        print(classification_report(y_test, y_pred))
    except Exception:
        print(classification_report(y_test, y_pred, zero_division=0))

    # Feature importance
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        features = X.columns

        feature_df = pd.DataFrame({
            "Feature": features,
            "Importance": importances
        }).sort_values(by="Importance", ascending=False)

        print("\nTop 10 Important Features:")
        print(feature_df.head(10).to_string(index=False))

        # save feature importances
        fi_dir = os.path.dirname(save_model_path)
        os.makedirs(fi_dir, exist_ok=True)
        fi_path = os.path.join(fi_dir, "feature_importances.csv")
        feature_df.to_csv(fi_path, index=False)
        print(f"Saved feature importances to {fi_path}")
    else:
        print("Model does not expose feature_importances_. Skipping.")

    # Save model
    os.makedirs(os.path.dirname(save_model_path), exist_ok=True)
    joblib.dump(model, save_model_path)
    print(f"Saved trained model to {save_model_path}")


def _parse_args():
    parser = argparse.ArgumentParser(description="Train FD-XIDS Random Forest model")
    parser.add_argument(
        "--data",
        type=str,
        default=os.path.join("..", "data", "processed", "train_processed.csv"),
        help="Path to processed training CSV"
    )
    parser.add_argument(
        "--save",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "saved_models", "fd_xids_model.pkl"),
        help="Path to save trained model"
    )
    parser.add_argument(
        "--tune",
        action="store_true",
        help="Enable GridSearch hyperparameter tuning"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), args.data)) if not os.path.isabs(args.data) else args.data
    save_path = args.save

    # If the provided data path doesn't exist relative to this file, try project root
    if not os.path.exists(data_path):
        alt = os.path.abspath(os.path.join(os.getcwd(), args.data))
        if os.path.exists(alt):
            data_path = alt

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Processed training data not found at {data_path}")

    train_fd_xids_model(data_path, save_path, tune=args.tune)

