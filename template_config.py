def spectral_type(T):
    """Approximate stellar spectral class from effective temperature."""
    if T < 3700: return "M"
    if T < 5200: return "K"
    if T < 6000: return "G"
    if T < 7500: return "F"
    return "A"

def generate_config_text(params, name, period_days):
    return f"""<OBJECT>Exoplanet
<OBJECT-NAME>{name}
<OBJECT-DIAMETER>{params["diameter_km"]:.1f}
<OBJECT-GRAVITY>{params["gravity_ms2"]:.2f}
<OBJECT-STAR-TEMPERATURE>{params["star_temp_K"]:.1f}
<OBJECT-STAR-TYPE>{spectral_type(params["star_temp_K"])}
<OBJECT-PERIOD>{period_days:.6f}
<OBJECT-INCLINATION>{params["inclination_deg"]:.2f}
<OBJECT-ORBIT>{params["semi_major_AU"]:.6f},0.00000,{period_days:.6f},0.00000,0.00000,2454979.033030
<SURFACE-PRESSURE>{params["surface_pressure_bar"]:.2f}
<ATMOSPHERE-GAS>CO2,N2
<ATMOSPHERE-ABUN>{params["co2_frac"]:.2f},{params["n2_frac"]:.2f}
<GENERATOR-RANGE1>0.5
<GENERATOR-RANGE2>17
<GENERATOR-RESOLUTION>200
<GENERATOR-NOISE>CCD
"""