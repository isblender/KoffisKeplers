import os
import subprocess
import time

# ─── CONFIG ──────────────────────────────────────────────────────────────
INPUT_DIR   = "configs"        # ← updated: where your *_cfg_no_gen.txt actually lives
OUT_DIR     = "full_output"           # where to dump the full outputs
API_URL     = "https://psg.gsfc.nasa.gov/api.php"
SLEEP_SEC   = 1                       # pause between calls
# ─────────────────────────────────────────────────────────────────────────

os.makedirs(OUT_DIR, exist_ok=True)

for fname in os.listdir(INPUT_DIR):
    # only pick your no-gen config files
    if not fname.endswith("_cfg.txt"):
        continue

    planet    = fname.replace("_cfg.txt", "")
    cfg_path  = os.path.join(INPUT_DIR, fname)
    out_path  = os.path.join(OUT_DIR, f"{planet}_all.txt")

    # build the curl command
    cmd = [
        "curl", "-s",
        "-d", "type=all",
        "--data-urlencode", f"file@{cfg_path}",
        API_URL
    ]

    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        output = res.stdout

        # skip if nothing meaningful came back
        if len(output) < 100:
            print(f"⚠️  {planet}: no data returned, skipping.")
            continue

        # save the full config + spectra
        with open(out_path, "w") as f_out:
            f_out.write(output)
        print(f"✅ Saved full output for {planet} → {out_path}")

    except subprocess.TimeoutExpired:
        print(f"⏱️  Timeout for {planet}, skipping.")
    except Exception as e:
        print(f"❌  Error for {planet}: {e}")

    time.sleep(SLEEP_SEC)