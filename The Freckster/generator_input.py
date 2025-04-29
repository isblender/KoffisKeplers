import glob
import os

# 1) The block you want to append to every config
instrument_block = """
<GENERATOR-RANGE1>0.4
<GENERATOR-RANGE2>20
<GENERATOR-RANGEUNIT>um
<GENERATOR-RESOLUTION>200
<GENERATOR-RESOLUTIONUNIT>RP

<GENERATOR-TELESCOPE>SINGLE
<GENERATOR-DIAMTELE>5.64
<GENERATOR-BEAM>1.0
<GENERATOR-BEAM-UNIT>diffrac

<GENERATOR-GAS-MODEL>Y
<GENERATOR-CONT-MODEL>Y
<GENERATOR-CONT-STELLAR>N
<GENERATOR-TRANS-APPLY>N
<GENERATOR-TRANS-SHOW>N
<GENERATOR-RADUNITS>ppm
<GENERATOR-RESOLUTIONKERNEL>Y

<!-- If you want noise (optional): -->
<NOISE-MODEL>Y
<NOISE-SNR>50
"""

# 2) Your input folder of “no-gen” configs
IN_DIR  = "configs_no_gen"
# 3) Where you want the fully-built configs to live
OUT_DIR = "configs"
os.makedirs(OUT_DIR, exist_ok=True)

# 4) Grab every *_cfg_no_gen.txt
pattern = os.path.join(IN_DIR, "*_cfg_no_gen.txt")
for in_path in glob.glob(pattern):
    # read the original
    with open(in_path, "r") as f:
        contents = f.read()

    # build an output filename:
    # e.g. GJ_1214b_cfg_no_gen.txt → GJ_1214b_cfg.txt
    base = os.path.basename(in_path)
    new_name = base.replace("_cfg_no_gen.txt", "_cfg.txt")
    out_path = os.path.join(OUT_DIR, new_name)

    # write the copy + appended block
    with open(out_path, "w") as f:
        f.write(contents)
        f.write(instrument_block)

    print(f"✅  Wrote {out_path}")