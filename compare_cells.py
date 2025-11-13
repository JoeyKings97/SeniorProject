from tower_cell import TowerCellInputs, compute_cell_balance, annual_gallons_from_gpm, annual_water_cost_usd

def summarize(cells):
    results = [compute_cell_balance(inp) for inp in cells]
    total_recovered_gpm = sum(r.recovered_gpm for r in results)
    total_makeup_gpm = sum(r.net_makeup_gpm for r in results)
    annual_rec_gal = annual_gallons_from_gpm(total_recovered_gpm)
    annual_savings = annual_water_cost_usd(annual_rec_gal, price_per_kgal=6.00)
    return{
        "cells": len(cells),
        "recovered_gpm": total_recovered_gpm,
        "makeup_gpm": total_makeup_gpm,
        "annual_recovered_gal": annual_rec_gal,
        "annual_$saved": annual_savings
    }

# Option A: One-Cell, Higher Efficiency
optA_cells = [
    TowerCellInputs(flow_gpm=100_000, delta_t_f=20.0, recovery_eff_frac=0.60, drift_rate_frac=0.001, blowdown_ratio_to_evap=0.25)
]

# Option B: 2 cell, modest efficiency/cell
optB_cells = [
    TowerCellInputs(flow_gpm=100_000, delta_t_f=20.0, recovery_eff_frac=0.45, drift_rate_frac=0.001, blowdown_ratio_to_evap=0.25),
    TowerCellInputs(flow_gpm=100_000, delta_t_f=20.0, recovery_eff_frac=0.45, drift_rate_frac=0.001, blowdown_ratio_to_evap=0.25),
]

A = summarize(optA_cells)
B = summarize(optB_cells)

for name, data in [("Option A (Single Cell)", A), ("Option B (Two Cells)", B)]:
    print(f"\n{name}")
    print(f"  Cells simulated:     {data['cells']}")
    print(f"  Recovered water:     {data['recovered_gpm']} gpm")
    print(f"  Net makeup:          {data['makeup_gpm']} gpm")
    print(f"  Annual recovered:    {data['annual_recovered_gal']} gallons")
    print(f"  Annual $ saved:      ${data['annual_$saved']}")