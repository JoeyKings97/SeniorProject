import csv
import random
import sys
from pathlib import Path

# ------------------------------------------------
# Ensure we can import tower_cell.py at project root
# ------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from tower_cell import TowerCellInputs, compute_cell_balance


# Where to save dataset
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_PATH = DATA_DIR / "ml_dataset.csv"


def sample_climate_conditions():
    """
    Generate realistic climate ranges needed for WERC analysis.
    """
    dry_bulb_f = random.uniform(40.0, 110.0)
    rel_humidity_pct = random.uniform(5.0, 60.0)
    wind_m_s = random.uniform(0.0, 10.0)
    month = random.randint(1, 12)

    return dry_bulb_f, rel_humidity_pct, wind_m_s, month


def estimate_recovery_efficiency(dry_bulb_f: float, rel_humidity_pct: float) -> float:
    """
    Synthetic mapping from climate → expected recovery efficiency.
    ML will learn this relationship from synthetic data.
    """
    base_eff = 0.60
    rh_factor = rel_humidity_pct / 60.0
    temp_penalty = max(0.0, (dry_bulb_f - 80.0) / 40.0)

    eff = base_eff * (0.5 + 0.5 * rh_factor) * (1.0 - 0.35 * temp_penalty)
    eff = max(0.0, min(0.95, eff))

    return eff


def main(n_samples: int = 3000) -> None:
    print(f"Writing ML dataset to: {DATA_PATH.resolve()}")

    fieldnames = [
        "dry_bulb_f",
        "rel_humidity_pct",
        "wind_m_s",
        "month",
        "recovery_eff_frac",
        "evap_gpm",
        "drift_gpm",
        "blowdown_gpm",
        "recovered_gpm",
        "net_makeup_gpm",
        "recovery_pct_of_evap",
    ]

    with DATA_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(n_samples):
            dry_bulb_f, rh_pct, wind_m_s, month = sample_climate_conditions()
            recovery_eff = estimate_recovery_efficiency(dry_bulb_f, rh_pct)

            inp = TowerCellInputs(
                flow_gpm=100_000.0,
                delta_t_f=20.0,
                recovery_eff_frac=recovery_eff,
                drift_rate_frac=0.001,
                blowdown_ratio_to_evap=0.25,
            )

            result = compute_cell_balance(inp)

            writer.writerow({
                "dry_bulb_f": dry_bulb_f,
                "rel_humidity_pct": rh_pct,
                "wind_m_s": wind_m_s,
                "month": month,
                "recovery_eff_frac": recovery_eff,
                "evap_gpm": result.evap_gpm,
                "drift_gpm": result.drift_gpm,
                "blowdown_gpm": result.blowdown_gpm,
                "recovered_gpm": result.recovered_gpm,
                "net_makeup_gpm": result.net_makeup_gpm,
                "recovery_pct_of_evap": result.recovery_pct_of_evap,
            })

            if (i + 1) % 200 == 0:
                print(f"Generated {i + 1}/{n_samples} samples")

    print("\n ML dataset generation complete!")


if __name__ == "__main__":
    main()
