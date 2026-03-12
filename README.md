# SCL2205: Sub-cellular Localisation Dataset

[![Test Suite](https://github.com/ousodaniel/scldata/actions/workflows/test.yaml/badge.svg)](https://github.com/ousodaniel/scldata/actions/workflows/test.yaml)
[![PyPI version](https://badge.fury.io/py/p-scldata.svg)](https://badge.fury.io/py/p-scldata)
[![Python versions](https://img.shields.io/pypi/pyversions/p-scldata.svg)](https://pypi.org/project/p-scldata/)
[![codecov](https://codecov.io/gh/ousodaniel/scldata/branch/main/graph/badge.svg)](https://codecov.io/gh/ousodaniel/scldata)
![Data](https://img.shields.io/badge/Data-Sub--cellular%20Localisation-blue?style=for-the-badge&logo=moleculer&logoColor=blue)
![Mol Type](https://img.shields.io/badge/Mol--type-Protein%20Sequence-green?style=for-the-badge&logo=moleculer&logoColor=green)

An installable dataset package for subcellular localisation prediction modelling.
It is suitable for clustering, classification, and generative protein language machine learning, and comprises dataset tracks for the `train-valid-test` and `cross-validation-test` (`k = 5`) model development approaches.
Preprocessing is already done, including homology reduction within and across corresponding splits.
Motivated by the `F.A.I.R` principle.

**Interface:** `Python` package with `CLI`

**Installation:**

*Package manager:* `pip install p-scldata`. Available as `scldata` after installation


**Example usage:**
```
# Python
>>> import scldata.loader as sdl # load pkg
>>> data_struct = sdl.load() # default, the full dataset structure
>>> df_train = sdl.load("train") # returns the training split
>>> fasta_file = sdl.load('test', fasta=True) # returns a StringIO handle

# CLI
$ scldata # default, returns the help page
$ scldata --split train # return training  split in deafault .tsv format
$ scldata --split train --format fasta # returns the full training split in FASTA
$ scldata --info struct # overview of the dataset
$ scldata --help # for other options
```

**Description:** This dataset comprises 19074 protein sequences (`col 1`) and corresponding subcellular localisation labels (`col 2`), covering 13 classes (nine single-location and four multi-location classes). `col 1` serves as the predictor (`input`), while `col 2` is the target (`output`)

**Structure:** unarchived and decompressed folder layout

```
scldata
└── data
    ├── entries.json # contains the UniProtKB unique "entry" identifier index
    ├── labels.json # contains the mined UniProtKB  "cellular component" location bi-directional index: 13 locations; 9 single and 4 multi
    ├── scl2205.csv # contains the full dataset in comma-separated-values (.csv) format
    └── splits.json # contains the partitioning of the full dataset as index lists of records constituting each partition
```

**Components:**

1. ***entries.json***: `key=value` pairs; `key` is integer index, `value` is UniProtKB unique identifier.
2. ***labels.json***: nested `key=value` pairs;  `key` is integer index, `value` is subcellular location for the `index_to_label` key-index, and vice versa for the `label_to_index` key-index.
3. ***scl2205.csv***:
   * Column 0: Table index; name, `entry`; type `str`
   * Column 1: Protein sequence (X variable); name, `seq`; type `str`
   * Column 2: Subcellular location (Y variable); name `scl`; type `str`
4. ***splits.json***
   * Abbreviations
     * `cv`: cross-validation (the 5-fold cross-validation dataset)
     * `fk`: fold `k`; ranges from zero to four
     * `trn`: training split
     * `tst`: the `heldout` evaluation set
     * `vld`: validation split (for monitoring training) _aka_ `development` or `discovery`
     * `[<int index>, ...]`: list of integer indices representing partition members
5. **Classes:**
   1. Cytoplasm (`CYT`)
   2. Plastid (`PLA`)
   3. Secreted (`SEC`)
   4. Mitochondrion (`MIT`)
   5. Membrane (`MEM`)
   6. Peroxisome (`PER`)
   7. Nucleus (`NUC`)
   8. Cell projection (`CEP`)
   9. ER (`ER`)
   10. Cytoplasm;Nucleus (`CYT;NUC`)
   11. Centrosome;Cytoplasm;Cytoskeleton;Microtubule organizing center (`CEN;CYT;CYTS;MTOC`)
   12. Cytoplasm;Membrane (`CYT;MEM`)
   13. Cytoplasm;Cytoskeleton (`CYT;CYTS`)

```
splits
├── cv
│   ├── f0
│   │   ├── trn = [<int index>, ...] # counts: 15187
│   │   └── vld = [<int index>, ...] # counts: 1256
│   ├── f1
│   │   ├── trn = [<int index>, ...] # counts: 15203
│   │   └── vld = [<int index>, ...] # counts: 1240
│   ├── f2
│   │   ├── trn = [<int index>, ...] # counts: 15185
│   │   └── vld = [<int index>, ...] # counts: 1258
│   ├── f3
│   │   ├── trn = [<int index>, ...] # counts: 15210
│   │   └── vld = [<int index>, ...] # counts: 1233
│   └── f4
│       ├── trn = [<int index>, ...] # counts: 15265
│       └── vld = [<int index>, ...] # counts: 1178
├── vld = [<int index>, ...] # counts: 15183
├── trn = [<int index>, ...] # counts: 1260
└── tst = [<int index>, ...] # counts: 2631
```

**Notes:**

1. No missing values

## Code/software

An open-source Python package for the data, `p-scldata`, is available on the official Python Package Index (PyPI). Upon installation, the dataset is automatically downloaded, and users can preview the data or load specific partitions programmatically (in the command line or as an import). The package is under active development, with additional features planned for future releases.

## Other raw data access information

Other publicly accessible locations of the raw data:

* DRYAD: [Coming...]()
* Zenodo: [Coming...]()
* Hugging Face: [Coming...]()

Data was derived from the following sources:

* UniProtKB (release 2022\_05; 20230124): [https://www.uniprot.org/](https://www.uniprot.org/)

## Changelog

See [CHANGELOG.md](https://github.com/ousodaniel/scldata/blob/main/CHANGELOG.md) for version history.
