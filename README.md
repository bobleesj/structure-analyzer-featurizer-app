# Structure Featurizer Analyzer (SAF) command-line interactive application

This is a command-line interactive app for `SAF` that allows you to generate features easily.

> For more information, please visit https://github.com/bobleesj/structure-analyzer-featurizer for the official documentation and feature list.

## Getting started

Install `SAF`:

```bash
pip install structure-analyzer-featurizer
```

Then run:

```bash
python main.py
```

You will be prompted with the following:

```bash
Folders with .cif files detected:
1. 20240902_PCD_demo_files (20 files)
2. 20240902_ICSD_demo_files (20 files)

Would you like to process each folder above sequentially?
(Default: Y) [Y/n]:
```

At the end, `.csv` files will be saved in the chosen project directory, including `csv/<composition-type>_features.csv` and `csv/universal_features.csv`.
