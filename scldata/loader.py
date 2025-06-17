import json
import pandas as pd
from typing import Tuple, Union

def load(split: Union[str, int, None] = None) -> Union[pd.DataFrame, Tuple[pd.DataFrame]]:
    df_full = pd.read_csv('data/scl2205.csv', index_col='entry')

    if split is None or split == 'full':
        return df_full

    with open('data/splits.json', 'r') as f:
        splits = json.load(f)

    with open('data/entries.json', 'r') as f:
        entries = json.load(f)

    if split == 'train':
        return df_full.loc[[entries[str(idx)] for idx in splits['trn']]]
    elif split == 'eval':
        return df_full.loc[[entries[str(idx)] for idx in splits['evl']]]
    elif split == 'heldout':
        return df_full.loc[[entries[str(idx)] for idx in splits['tst']]]
    elif (isinstance(split, int) or int(split)) and int(split) in range(5):
        k = int(split)
        return (df_full.loc[[entries[str(idx)] for idx in splits['cv'][f'f{k}']['trn']]],
                df_full.loc[[entries[str(idx)] for idx in splits['cv'][f'f{k}']['tst']]])
    else:
        raise ValueError('split must be either None, full, train, eval, heldout or an integer(-string) representing a k-fold split ')
