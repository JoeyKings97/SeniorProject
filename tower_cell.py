from dataclasses import dataclass
from typing import Optional

@dataclass
class TowerCellInputs:
    flow_gpm: float
    delta_t_f: float
    recovery_eff_frac: float
    drift_rate_frac: float = 0.001
    blowdown_ratio_to_evap: float = 0.25

@dataclass
class TowerCellResult:
    evap_gpm: float
    drift_gpm: float
    blowdown_gpm: float
    recovered_gpm: float
    net_makeup_gpm: float
    recovery_pct_of_evap: float

def evap_rule_of_thumb_gpm(flow_gpm: float, delta_t_f: float) -> float:
    """
    WERC citates rule of thumb: 1% of recirc. flow evap/ 10 Degree F cooling.
    """
    return flow_gpm * (0.01 * (delta_t_f / 10.0))

def compute_cell_balance(inp: TowerCellInputs) -> TowerCellResult:
    evap = evap_rule_of_thumb_gpm(inp.flow_gpm, inp.delta_t_f)
    drift = inp.flow_gpm * inp.drift_rate_frac
    blowdown = evap * inp.blowdown_ratio_to_evap

    # WERC design: recovery targets evap only.
    # other losses can be tracked but are disregarded.
    recovered = evap * max(0.0, min(inp.recovery_eff_frac, 0.95))

    net_makeup = evap + drift + blowdown - recovered
    recovery_pct = 0.0 if evap == 0 else (recovered / evap) * 100.0

    return TowerCellResult(
        evap_gpm=evap,
        drift_gpm=drift,
        blowdown_gpm=blowdown,
        recovered_gpm=recovered,
        net_makeup_gpm=net_makeup,
        recovery_pct_of_evap=recovery_pct,
    )

def annual_gallons_from_gpm(gpm: float) -> float:
    return gpm * 60.0 * 24.0 * 365.0

def annual_water_cost_usd(gal: float, price_per_kgal: float = 6.00) -> float:
    # Standard: $6.00/1000 gal
    return (gal / 1000.0) * price_per_kgal