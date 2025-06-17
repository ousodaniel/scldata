import json
import pandas as pd
from typing import Tuple, Union

with open('data/labels.json', 'r') as f:
    labels = json.load(f)

with open('data/splits.json', 'r') as f:
    splits = json.load(f)

with open('data/entries.json', 'r') as f:
    entries = json.load(f)

def load(split: Union[str, int, None] = None) -> Union[pd.DataFrame, Tuple[pd.DataFrame]]:
    """
    A function for loading the full or split SCL2205 dataset.

    Parameters
    ----------
    `split`: `str` | `int`, optional

    :param split: `str` or `int` or `None`. If `str`, it can be either of "full", "train", "eval", "heldout". Integers can be provided in string form.

    Returns
    -------
    `pandas.DataFrame`

    :return: A `Pandas DataFrame` with UniProtKB unique entries as indices. The first column is "seq" (protein sequence), and the second is "scl" (subcellular location).

    Descriptions
    -----

    SCL2205
        The dataset name: SubCellularLocalisation and 2205 represents the UniProtKB release year (YY) and month (M).
    full : str
        The complete, unsplit SCL2205 dataset.
    train : str
        The part of SCL2205 used for model training in the *train-eval-test* model development approach.
    eval : str
        The part of SCL2205 used for model evaluation during training in the *train-eval-test* model development approach.
    heldout : str
        The part of SCL2205 used only for the **final** (internal) model testing.
    k : int | str
        The value of the "split" param specifying a fold split of the SCL2205 dataset in the k-fold cross-validation model development approach. An integer string may be provided.

    .. _UniProtKB: `https://uniprot.org/`

    Citations
    ---------

    Examples
    --------
    >>> import scldata as sd
    >>> df_full = sd.load("full")
    >>> df_full = sd.load()
    >>> df_train = sd.load("train")
    >>> df_eval = sd.load("eval")
    >>> df_heldout = sd.load("heldout")
    >>> df_kfold0 = sd.load(0) # retuns a tuple of dataframes with training and testing sets at index 0 and 1, respectively
    >>> df_kfold0 = sd.load("0")

    .. note:: The SCL2205 dataset was curated from `UniProtKB`_, the latest release as of 24/01/2023. The indices are persistent identifiers consistent with *UniProtKB entry* feature.

    """

    df_full = pd.read_csv('data/scl2205.csv', index_col='entry')

    if split is None or split == 'full':
        return df_full.replace(labels)
    elif split == 'train':
        return df_full.loc[[entries[str(idx)] for idx in splits['trn']]].replace(labels)
    elif split == 'eval':
        return df_full.loc[[entries[str(idx)] for idx in splits['evl']]].replace(labels)
    elif split == 'heldout':
        return df_full.loc[[entries[str(idx)] for idx in splits['tst']]].replace(labels)
    elif (isinstance(split, int) or int(split)) and int(split) in range(5):
        k = int(split)
        return (df_full.loc[[entries[str(idx)] for idx in splits['cv'][f'f{k}']['trn']]].replace(labels),
                df_full.loc[[entries[str(idx)] for idx in splits['cv'][f'f{k}']['tst']]].replace(labels))
    else:
        raise ValueError('split must be either None, "full", "train", "eval", "heldout" or an integer(-string) representing a k-fold split, eg. 0 0r "0"')
