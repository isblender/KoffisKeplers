import os
import pandas as pd
from io import StringIO

# --- CONFIG ---
FULL_OUT_DIR = "full_output"    # where your *_all.txt live
TRN_OUT_DIR  = "spectra_trn"    # target folder for the .csvs
os.makedirs(TRN_OUT_DIR, exist_ok=True)

# --- MAIN LOOP ---
for fname in os.listdir(FULL_OUT_DIR):
    if not fname.endswith("_all.txt"):
        continue

    planet = fname.replace("_all.txt", "")
    full_path = os.path.join(FULL_OUT_DIR, fname)

    # 1) read all lines
    with open(full_path, "r") as f:
        lines = f.readlines()

    # 2) locate the "results_trn.txt" header
    try:
        start_idx = next(
            i for i, L in enumerate(lines)
            if L.strip() == "results_trn.txt"
        )
    except StopIteration:
        print(f"⚠️  no trn section in {fname}, skipping")
        continue

    # 3) grab everything after that line
    trn_block = "".join(lines[start_idx+1:])

    # 4) parse it into a DataFrame (cols 0 & 1 only)
    df = pd.read_csv(
        StringIO(trn_block),
        sep=r"\s+",
        header=None,
        comment="#",
        usecols=[0, 1],
        names=["Wavelength_um", "Total_T"]
    )
    df["Planet"] = planet

    # 5) write out to CSV
    out_csv = os.path.join(TRN_OUT_DIR, f"{planet}_trn.csv")
    df.to_csv(out_csv, index=False)
    print(f"✅  wrote {out_csv}")


import pandas as pd
import matplotlib.pyplot as plt

# 1) Point this to your CSV
csv_path = "spectra_trn/Kelt-9_b_trn.csv"

# 2) Load it
df = pd.read_csv(csv_path)

# 3) Plot
plt.figure(figsize=(8, 5))
plt.plot(df["Wavelength_um"], df["Total_T"], lw=1.5)
plt.xlabel("Wavelength (µm)")
plt.ylabel("Total Transmittance")
plt.title("GJ 1214 b Transmittance Spectrum")
plt.grid(True)
plt.tight_layout()
plt.show()