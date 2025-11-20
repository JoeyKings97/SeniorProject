import sys
from pathlib import Path
import numpy as np
import joblib

# -----------------------------
# Paths
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "ml" / "models" / "random_forest.joblib"

# WERC water cost assumption: $6.00 per 1000 gallons
WATER_COST_PER_KGAL = 6.00


def load_model():
    """Load the trained Random Forest model from models/ folder."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. "
            "Run ml_train_models.py first."
        )
    return joblib.load(MODEL_PATH)


def predict_recovery(
    dry_bulb_f: float,
    rel_humidity_pct: float,
    wind_m_s: float,
    month: int,
    recovery_eff_frac: float,
    hours_per_year: float = 8760.0,
):
    """
    Predict recovered water (gpm), annual gallons, and annual cost savings.
    """
    model = load_model()

    x = np.array(
        [[dry_bulb_f, rel_humidity_pct, wind_m_s, month, recovery_eff_frac]],
        dtype=float,
    )

    recovered_gpm = float(model.predict(x)[0])

    gallons_per_year = recovered_gpm * 60.0 * hours_per_year
    thousands_gallons = gallons_per_year / 1000.0
    annual_savings_usd = thousands_gallons * WATER_COST_PER_KGAL

    return recovered_gpm, gallons_per_year, annual_savings_usd


def main():
    print("=== Cooling Tower Water Recovery ML Predictor ===")

    dry_bulb_f = float(input("Ambient temperature (°F): "))
    rel_humidity_pct = float(input("Relative humidity (%): "))
    wind_m_s = float(input("Wind speed (m/s): "))
    month = int(input("Month [1-12]: "))
    recovery_eff_frac = float(input("Retrofit recovery efficiency (0–1): "))

    recovered_gpm, gallons_year, savings_year = predict_recovery(
        dry_bulb_f,
        rel_humidity_pct,
        wind_m_s,
        month,
        recovery_eff_frac,
    )

    print("\n--- Prediction ---")
    print(f"Recovered water rate: {recovered_gpm:.2f} gpm")
    print(f"Annual water recovered: {gallons_year:,.0f} gallons/year")
    print(
        f"Annual water savings (@ ${WATER_COST_PER_KGAL:.2f}/kgal): "
        f"${savings_year:,.0f} per year"
    )


if __name__ == "__main__":
    main()
