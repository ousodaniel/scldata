import json

import pandas as pd
from typing import Tuple, Union
from pathlib import Path

def load(split: Union[str, int, None] = None) -> Union[pd.DataFrame, Tuple[pd.DataFrame]]:
    df_full = pd.read_csv('data/scl2205.csv', index_col='entry')

    if split is None or split == 'full':
        return df_full
