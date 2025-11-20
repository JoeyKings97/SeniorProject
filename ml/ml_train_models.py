import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# -----------------------------
# Paths
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "ml_dataset.csv"
MODEL_DIR = ROOT / "ml" / "models"
MODEL_DIR.mkdir(exist_ok=True)

FEATURE_COLS = [
    "dry_bulb_f",
    "rel_humidity_pct",
    "wind_m_s",
    "month",
    "recovery_eff_frac",
]

TARGET_COL = "recovered_gpm"


def load_dataset():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Run ml_generate_dataset.py first."
        )
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]
    return X, y


def evaluate_model(name: str, y_true, y_pred) -> None:
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_true, y_pred)

    print(f"\n=== {name} ===")
    print(f"MAE  = {mae:.3f} gpm")
    print(f"RMSE = {rmse:.3f} gpm")
    print(f"R^2  = {r2:.3f}")


def main():
    X, y = load_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # -----------------------------
    # Linear Regression
    # -----------------------------
    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)
    y_pred_lin = lin_reg.predict(X_test)
    evaluate_model("Linear Regression", y_test, y_pred_lin)
    joblib.dump(lin_reg, MODEL_DIR / "linear_regression.joblib")

    # -----------------------------
    # Random Forest
    # -----------------------------
    rf = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    evaluate_model("Random Forest Regressor", y_test, y_pred_rf)
    joblib.dump(rf, MODEL_DIR / "random_forest.joblib")

    print(f"\n✅ Saved models in: {MODEL_DIR.resolve()}")


if __name__ == "__main__":
    main()
