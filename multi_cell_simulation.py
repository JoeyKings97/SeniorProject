from tower_cell import TowerCellInputs, compute_cell_balance, annual_gallons_from_gpm, annual_water_cost_usd

def summarize(cells):
    """Compute total water recovery and cost for a list of cells."""
    results = [compute_cell_balance(inp) for inp in cells]
    total_recovered_gpm = sum(r.recovered_gpm for r in results)
    total_makeup_gpm = sum(r.net_makeup_gpm for r in results)
    annual_rec_gal = annual_gallons_from_gpm(total_recovered_gpm)
    annual_savings = annual_water_cost_usd(annual_rec_gal, price_per_kgal=6.00)
    return {
        "cells": len(cells),
        "recovered_gpm": total_recovered_gpm,
        "makeup_gpm": total_makeup_gpm,
        "annual_recovered_gal": annual_rec_gal,
        "annual_$saved": annual_savings
    }

def run_multi_cell(num_cells: int, flow_gpm=100_000, delta_t_f=20.0,
                   recovery_eff_frac=0.60, drift_rate_frac=0.001,
                   blowdown_ratio_to_evap=0.25):
    """Generate identical cells and compute totals for N-cell configuration."""
    cells = [
        TowerCellInputs(
            flow_gpm=flow_gpm,
            delta_t_f=delta_t_f,
            recovery_eff_frac=recovery_eff_frac,
            drift_rate_frac=drift_rate_frac,
            blowdown_ratio_to_evap=blowdown_ratio_to_evap
        )
        for _ in range(num_cells)
    ]
    return summarize(cells)

# --- Example usage ---
if __name__ == "__main__":
    # Try different tower configurations
    for n in [1, 2, 6, 18]:
        result = run_multi_cell(num_cells=n)
        print(f"\nSimulation for {n} cooling tower cell(s):")
        print(f"  Recovered water:     {result['recovered_gpm']} gpm")
        print(f"  Net makeup:          {result['makeup_gpm']} gpm")
        print(f"  Annual recovered:    {result['annual_recovered_gal']} gallons")
        print(f"  Annual $ saved:      ${result['annual_$saved']}")
