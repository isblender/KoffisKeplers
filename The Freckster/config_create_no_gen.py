import os
import time
import subprocess
import pandas as pd
from datetime import datetime

# Constants
NASA_TAP = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    "?query=select+pl_name+from+pscomppars&format=csv"
)

PSG_API_URL = "https://psg.gsfc.nasa.gov/api.php"

planets_df = pd.read_csv(NASA_TAP)
planet_names = ["GJ 1214b"] + ["Kelt-9 b"] + planets_df['pl_name'].dropna().tolist()

OUT_DIR = "configs_no_gen"
os.makedirs(OUT_DIR, exist_ok=True)
MIN_DIR = "min_configs"
os.makedirs(MIN_DIR, exist_ok=True)

for planet in planet_names:
    safe = planet.replace(" ", "_").replace("/", "_")
    cfg_path = os.path.join(MIN_DIR, f"{safe}_minimal_cfg.txt")
    out_path = os.path.join(OUT_DIR, f"{safe}_cfg_no_gen.txt")

    date = datetime(2020, 4, 8, 1, 32).strftime("%Y/%m/%d %H:%M")
    date = datetime.now().strftime("%Y/%m/%d %H:%M")

    with open(cfg_path, "w") as f:
        f.write(f"<OBJECT>Exoplanet\n")
        f.write(f"<OBJECT-NAME>{planet}\n")
        f.write(f"<OBJECT-DATE>{date}\n")

    cmd = [
        "curl", "-s",
        "-d", "type=cfg",
        "-d", "wcfg=y",
        "-d", "wephm=y",
        "-d", "watm=y",
        "-d", "whdr=n",
        "-d", "wgeo=y",
        "-d", "wgen=y",  # ← add this
        "--data-urlencode", f"file@{cfg_path}",
        PSG_API_URL
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        output = res.stdout

        # Optional: skip if empty or too small
        if len(output) < 100:
            print(f"⚠️  {planet}: no data returned, skipping.")
            continue

        # 3c) Save the full config + all spectra
        with open(out_path, "w") as out:
            out.write(output)
        print(f"✅  Saved all outputs for {planet} → {out_path}")

    except subprocess.TimeoutExpired:
        print(f"⏱️  Timeout for {planet}, skipping.")
    except Exception as e:
        print(f"❌  Error for {planet}: {e}")

    # 3d) Be nice to the server
    time.sleep(1)

