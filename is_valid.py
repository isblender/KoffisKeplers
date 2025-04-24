import numpy as np

# Physical constants
G = 6.67430e-11       # m^3 kg^-1 s^-2
R_EARTH = 6371e3      # m
R_SUN = 6.9634e8      # m
M_SUN = 1.9885e30     # kg
AU = 1.495978707e11   # m

# --- Physical calculations ---
def compute_mass(params):
    R = (params["diameter_km"] * 1e3) / 2
    return params["gravity_ms2"] * R**2 / G


def compute_density(params):
    M = compute_mass(params)
    R = (params["diameter_km"] * 1e3) / 2
    return M / ((4/3) * np.pi * R**3)


def compute_equilibrium_temp(params):
    R_star = params["star_radius_Rsun"] * R_SUN
    a = params["semi_major_AU"] * AU
    return params["star_temp_K"] * np.sqrt(R_star / (2 * a))

# --- Filters ---
def check_hard_filters(params):
    # Density regime: rocky vs. gaseous
    rho = compute_density(params)
    if params["diameter_km"] < 2 * (R_EARTH / 1e3):  # rocky threshold ~2 R_earth
        if not (2000 < rho < 8000):
            return False
    else:
        if not (100 < rho < 2000):
            return False

    # Equilibrium temperature constraint
    Teq = compute_equilibrium_temp(params)
    if not (50 < Teq < 1000):
        return False

    # Surface pressure filter (1e-6 to 1e2 bar)
    P = params["surface_pressure_bar"]
    if not (1e-6 <= P <= 1e2):
        return False

    return True


def check_soft_filters(params):
    # Gas mixing ratio sums ≤ 1
    if params["co2_frac"] + params["n2_frac"] > 1.0:
        return False

    # Composition regimes
    R = (params["diameter_km"] * 1e3) / 2
    if R < 2 * R_EARTH:
        # Rocky worlds: CO2 ≤ 50%
        if params["co2_frac"] > 0.5:
            return False
    else:
        # Gas giants: N2 ≤ 30%
        if params["n2_frac"] > 0.3:
            return False

    # Temperature-driven composition constraints
    Teq = compute_equilibrium_temp(params)
    if Teq > 500 and params["co2_frac"] > 0.2:
        return False
    if Teq < 150 and params["co2_frac"] < 0.05:
        return False

    return True


def is_valid(params):
    """Return True if params pass both hard and soft filters."""
    return check_hard_filters(params) and check_soft_filters(params)
