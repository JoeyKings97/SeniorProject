import os
from tower_cell import TowerCellInputs, compute_cell_balance, annual_gallons_from_gpm, annual_water_cost_usd
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("outputs/inputs", exist_ok=True)

# 100k gpm/cell, deltaTemp = 20 degree F, 60% recovery efficiency
inp = TowerCellInputs(flow_gpm=100000, delta_t_f=20.0, recovery_eff_frac=0.60, drift_rate_frac=0.001, blowdown_ratio_to_evap=0.25)
res = compute_cell_balance(inp)
print("Evap gpm: ", res.evap_gpm)
print("Recovered gpm: ", res.recovered_gpm)
print("Net makeup gpm: ", res.net_makeup_gpm)

# Annual savings from recovered water
annual_saved_gal = annual_gallons_from_gpm(res.recovered_gpm)
annual_saved_usd = annual_water_cost_usd(annual_saved_gal, price_per_kgal=6.00)
print("Annual gallons recovered: ", f"{annual_saved_gal:,.0f}")
print("Annual $ saved:", f"${annual_saved_usd:,.0f}")

# Evap vs DeltaTemp for given flow
flow = 100000
delta_ts = np.arange(5, 30, 5)
evaps = [flow * (0.01 * (d/10.0)) for d in delta_ts]
plt.figure()
plt.plot(delta_ts, evaps, marker="o")
plt.xlabel("DeltaT across fill F")
plt.ylabel("Evaporation loss (gpm)")
plt.title("Single-cell Evap vs. DeltaT (Flow = 100,000 gpm)")
plt.grid(True)
plt.savefig("outputs/plots/evap_vs_deltaT.png", dpi=180)

# Annual $ saved vs. recovery efficiency
