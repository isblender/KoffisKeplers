import os
from io import StringIO
import pandas as pd


configs_dir = './content/configs'
if not os.path.exists(configs_dir):
    os.makedirs(configs_dir)

output_dir = './content/spectra'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Config files contain planetary info
# Searches 'configs' folder in collab to establish connection between config files and main directory

cfg_paths = [os.path.join(configs_dir, f) for f in os.listdir(configs_dir) if f.endswith('_cfg.txt')]

dfs = []

for path in cfg_paths:

    # Automatic initialization of output files that output PSG output in table form
    # Output data can be found in spectra folder
    filename = os.path.basename(path)
    planet_name = filename.replace('_cfg.txt', '')
    output_file = os.path.join(output_dir, f"{planet_name}.txt")

    # Transforms config files into PSG table output
    os.system(f'curl -d type=trn --data-urlencode file@{path} https://psg.gsfc.nasa.gov/api.php > {output_file}')

    with open(output_file, 'r') as fr:
        lines = fr.readlines()

    # Initializes column headers
    col_line = next(line for line in lines if line.strip().startswith('# Wave/freq'))
    col_names = col_line.strip('# \n').split()

    # This gets rid of header and comments
    data_lines = [line for line in lines if line.strip() and line[0].isdigit()]

    df = pd.read_csv(StringIO(''.join(data_lines)), sep=r'\s+', header=None)
    df.columns = col_names

    # Appends planet name to last column
    df['Planet'] = planet_name

    # Appends df to a list of dataframes
    dfs.append(df)

    print(df)