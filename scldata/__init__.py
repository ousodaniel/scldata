"""
    A dataset (SCL2205) package for subcellular localisation prediction modelling.
    Its use cases include clustering and classification machine learning, and contain dataset tracks for the *train-eval-test* and *cross-validation-test* (*k* = 5) model development approaches.
    Preprocessing is already done, including homology reduction within and across corresponding splits.

    Descriptions
    ------------
    SCL2205
        The dataset name: SubCellularLocalisation and 2205 represents the UniProtKB release year (YY) and month (M).

    Citations
    ---------

    Examples
    --------
    >>> import scldata.loader as sdl # or from scldata.loader import load or from scldata import load
    >>> df_full = sdl.load("full")
    >>> df_full = sdl.load()
    >>> df_train = sdl.load("train")
    >>> df_eval = sdl.load("eval")
    >>> df_heldout = sdl.load("heldout")
    >>> df_kfold0 = sdl.load(0) # retuns a tuple of dataframes with training and testing sets at index 0 and 1, respectively
    >>> df_kfold1_train = sdl.load("1")[0]

    .. note:: The SCL2205 dataset was curated from `UniProtKB`_, the latest release as of 24/01/2023. The indices are persistent identifiers consistent with *UniProtKB entry* identifier.

    .. _UniProtKB: `https://uniprot.org/`

"""
