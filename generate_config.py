import os
import numpy as np
import itertools

from is_valid import is_valid, G, M_SUN, AU
from template_config import generate_config_text

# Define the parameter space
param_ranges = {
    "diameter_km":        np.linspace(5000, 30000, 6),
    "gravity_ms2":        np.linspace(3, 25, 6),
    "star_temp_K":        np.linspace(3000, 7000, 5),
    "star_radius_Rsun":   np.linspace(0.5, 2.0, 4),
    "semi_major_AU":      np.linspace(0.03, 1.5, 5),
    "inclination_deg":    [90.0],
    "surface_pressure_bar":[0.1, 1, 10],
    "co2_frac":           [0.1, 0.5],
    "n2_frac":            [0.3, 0.6],
}

def main():
    os.makedirs("configs", exist_ok=True)
    count = 0
    keys, ranges = zip(*param_ranges.items())

    for idx, combo in enumerate(itertools.product(*ranges), start=1):
        params = dict(zip(keys, combo))
        if not is_valid(params):
            continue

        # Estimate stellar mass ∝ R_star^3
        M_star = (params["star_radius_Rsun"]**3) * M_SUN
        a = params["semi_major_AU"] * AU
        # Kepler's 3rd law
        period_s = 2 * np.pi * np.sqrt(a**3 / (G * M_star))
        period_days = period_s / 86400

        name = f"Exo_{idx}"
        cfg = generate_config_text(params, name, period_days)
        path = os.path.join("configs", f"{name}_cfg.txt")
        with open(path, "w") as f:
            f.write(cfg)

        count += 1

    print(f"Generated {count} valid PSG config files in ./configs/")

if __name__ == "__main__":
    main()