import json
import pandas as pd
from typing import Tuple, Union, TextIO, Optional
from pathlib import Path
from pandas import DataFrame

from scldata.utils.fasta_utils import seq_df_to_fasta_handle
from scldata.utils.scldata_summary import splits_str

_DATA_DIR = Path(__file__).parent / "data"

with open(f"{_DATA_DIR}/labels.json", "r") as f:
    labels = json.load(f)

with open(f"{_DATA_DIR}/splits.json", "r") as f:
    splits = json.load(f)

with open(f"{_DATA_DIR}/entries.json", "r") as f:
    entries = json.load(f)

df_full = pd.read_csv(f"{_DATA_DIR}/scl2205.csv", index_col="entry")


def load(
    split: Union[str, int, None] = None, fasta: Optional[bool] = False
) -> Union[
    str, DataFrame, TextIO, Tuple[Union[DataFrame, TextIO], Union[DataFrame, TextIO]]
]:
    """
    A function for loading the full or split SCL2205 dataset.

    Parameters
    ----------
    `split`: `str` | `int`, optional
    `fasta`: `bool`, optional

    :param split: `str` or `int` or `None`. If `str`, it can be either of "full", "train", "valid", "heldout" or "test". Integers can be provided in string form.
    :param fasta: `bool`, Whether to return a fasta file instead of a dataframe.

    Returns
    -------
    `pandas.DataFrame` | `TextIO handle`

    :return: A `Pandas DataFrame` with UniProtKB unique entries as indices. The first column is "seq" (protein sequence), and the second is "scl" (subcellular location). A `TextIO handle` for the fasta file equivalent, if `fasta` is `True`. A`tuple` of either types is returned if loading the cross-validation data splits.

    Descriptions
    -----`
    full : str
        The complete, unsplit SCL2205 dataset.
    train : str
        The part of SCL2205 used for model training in the *train-valid-test* model development approach.
    valid : str
        The part of SCL2205 used for model evaluation during training in the *train-valid-test* model development approach.
    heldout : str
        The part of SCL2205 used only for the **final** (internal) model testing.
    test : str
        Same as "heldout".
    k : int | str
        The value of the "split" param specifying a fold split of the SCL2205 dataset in the k-fold cross-validation model development approach. An integer string may be provided.

    """

    def format_output(df: pd.DataFrame) -> Union[pd.DataFrame, TextIO]:
        label_map = {int(k): v for k, v in labels["index_to_label"].items()}
        df = df.assign(scl=df.scl.map(label_map))
        return (
            seq_df_to_fasta_handle(df, description_col="scl", seq_col="seq")
            if fasta
            else df
        )

    if split is None:
        return splits_str
    elif split == "full":
        return format_output(df_full)
    elif split == "train":
        return format_output(df_full.loc[[entries[str(idx)] for idx in splits["trn"]]])
    elif split == "valid":
        return format_output(df_full.loc[[entries[str(idx)] for idx in splits["vld"]]])
    elif split == "heldout" or split == "test":
        return format_output(df_full.loc[[entries[str(idx)] for idx in splits["tst"]]])
    elif (isinstance(split, int) or isinstance(int(split), int)) and int(
        split
    ) in range(5):
        k = int(split)
        return (
            format_output(
                df_full.loc[[entries[str(idx)] for idx in splits["cv"][f"f{k}"]["trn"]]]
            ),
            format_output(
                df_full.loc[[entries[str(idx)] for idx in splits["cv"][f"f{k}"]["vld"]]]
            ),
        )
    else:
        raise ValueError(
            'split must be either None, "full", "train", "valid", "heldout", "test" or an integer(-string) representing a k-fold split, eg. 0 0r "0"'
        )


def load_label_encoding() -> str:
    return str(json.dumps(labels, indent=2))


def main():
    pass


if __name__ == "__main__":
    main()
