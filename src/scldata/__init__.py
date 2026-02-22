"""
    A dataset (SCL2205) package for subcellular localisation prediction modelling.
    Its use cases include clustering and classification machine learning, and contain dataset tracks for the *train-valid-test* and *cross-validation-test* (`k` = 5) model development approaches.
    Preprocessing is already done, including homology reduction within and across corresponding splits.

    The package also has a command line interface with additional capabilities: use the command `scldata`. Without any options, it prints out an equivalent of `DataFrame.head()`.

    Descriptions
    ------------
    SCL2205
        The dataset name: SubCellularLocalisation and 2205 represents the UniProtKB release year (YY) and month (M).

    Citations
    ---------

    Examples
    --------
    >>> import scldata as sdl
    >>> df_full = sdl.load('full')
    >>> df_full = sdl.load()
    >>> df_train = sdl.load('train')
    >>> df_valid = sdl.load('valid')
    >>> fasta_test_handle = sdl.load('test', fasta=True)
    >>> df_heldout = sdl.load('heldout') # "test" and "heldout" are interchangeable
    >>> df_kfold0 = sdl.load(0) # returns a tuple of dataframes with training and testing sets at index 0 and 1, respectively
    >>> df_kfold1_train = sdl.load('1')[0]

    .. note:: The SCL2205 dataset was curated from `UniProtKB`_, the latest release as of 24/01/2023. The indices are persistent identifiers consistent with *UniProtKB entry* identifier.

    .. _UniProtKB: `https://uniprot.org/`

"""
import argparse
import os
import sys
from io import TextIOBase, StringIO
from pandas import DataFrame
from importlib.metadata import version
from typing import TextIO, Tuple, Union

from scldata.loader import load
from scldata.utils.io_utils import OutputManager

__version__ = version('p-scldata')

from scldata.utils.scldata_summary import splits_str, label_abbr_dict


def output(out_manager: OutputManager, out: Union[str, DataFrame, TextIO, Tuple[Union[DataFrame, TextIO], Union[DataFrame, TextIO]]], fformat: str = None):
    """
    Writes output to the handle(s).

    Parameters
    ----------
    `out_manager`: `OutputManager`
    `out`: `Union[str, DataFrame, TextIO, Tuple[Union[DataFrame, TextIO]`
    `fformat`: `str`

    :param out_manager: `OutputManager`, The output manager object.
    :param out: `Union[str, DataFrame, TextIO, Tuple[Union[DataFrame, TextIO]`, The output manager object.
    :param fformat: `str`, The output file format, default None.

    Returns
    -------
    None
    """

    with out_manager as handle:
        if out_manager.count > 1:
            handle1 = handle[0]
            handle2 = handle[1]

        try:
            if fformat  and isinstance(out, TextIOBase):
                handle.write(out.read())
            elif fformat == 'fasta'  and isinstance(out, tuple):
                handle1.write(out[0].read())
                handle2.write(out[1].read())
            elif fformat == 'tsv' and isinstance(out, DataFrame):
                out.to_csv(handle, sep='\t', index=True)
            elif fformat == 'tsv' and isinstance(out, tuple):
                out[0].to_csv(handle1, sep='\t', index=True)
                out[1].to_csv(handle2, sep='\t', index=True)
            elif fformat == 'csv' and isinstance(out, DataFrame):
                out.to_csv(handle, sep=',', index=True)
            elif fformat == 'csv' and isinstance(out, tuple):
                out[0].to_csv(handle1, sep=',', index=True)
                out[1].to_csv(handle2, sep=',', index=True)
            elif not fformat:
                if isinstance(out, DataFrame):
                    out.to_csv(handle, sep='\t', index=True)
                elif isinstance(out, (str, TextIOBase)):
                    handle.write(out)
        except BrokenPipeError:
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
            sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(130)

def main():
    parser = argparse.ArgumentParser(prog='scldata',
                                     description='SCL2205 dataset loading to standard output. With no OPTION(s), outputs the HEAD of the full SCL2205 dataset.',
                                     usage='%(prog)s [OPTIONS]\nusage: %(prog)s [-h] [-s SPLIT] [-i INFO] [--scls] [--version] [-f FORMAT] [-o OUTPUT]\n\nFor more information, try "-h/--help".',
                                     epilog=(
                                         '\n'
                                         'Descriptions:\n'
                                         '  full : str\n'
                                         '    The complete, unsplit SCL2205 dataset.\n'
                                         '  train : str\n'
                                         '    The part of SCL2205 used for model training in the *train-valid-test* model development approach.\n'
                                         '  valid : str\n'
                                         '    The part of SCL2205 used for model evaluation during training in the *train-valid-test* model development approach.\n'
                                         '  heldout : str\n'
                                         '    The part of SCL2205 used only for the **final** (internal) model testing.\n'
                                         '  test : str\n'
                                         '    Same as "heldout".\n'
                                         '  k : int | str\n'
                                         '    The value of the "split" param specifying a fold split of the SCL2205 dataset in the k-fold cross-validation model development approach. An integer string may be provided.\n'
                                         '\n'
                                         'Examples:\n'
                                         '  scldata -h\n'
                                         '  scldata --split heldout # "test" is an alternative to "heldout"\n'
                                         '\n'
                                         'Homepage: https://github.com/ousodaniel/scldata\n'
                                         'Repository: https://github.com/ousodaniel/scldata.git\n'
                                         'Bug Tracker: https://github.com/ousodaniel/scldata/issues\n'
                                         '\n'
                                         'Maintainer: Ouso D. O. S. daniel.ouso[at]ucdconnect.ie'
                                     ),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,)
    parser.add_argument(
        '-s', '--split',
        type=str,
        default=None,
        choices=['train', 'valid', 'heldout', 'test', 'full', '0', '1', '2', '3', '4'],
        help='print which split to load: "train", "valid", "heldout", "test", "full", or k-fold ("0"-"4") (default: None).'
    )
    parser.add_argument(
        '-i', '--info',
        type=str,
        choices=['head', 'shape', 'struct'],
        default='head',
        help='print info: "head", "shape", or "struct" (default: "head")'
    )
    parser.add_argument(
        '-c', '--scls',
        type=str,
        choices=['full', 'long', 'short'],
        default=None,
        help='print scls target classes: "full", "long", "short" (default: None)'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'scldata {__version__}'
    )
    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['tsv', 'csv', 'fasta'],
        default='tsv',
        help='print output format: "tsv", "csv", or "fasta" (default: "tsv")',
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='-',
        help='print output file prefix (default: stdout)'
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    elif len(sys.argv) == 3 and (sys.argv[1] == '--info' or sys.argv[1] == '-i') and sys.argv[2] == 'head':
        print('Option "--info/-i head" must be accompanied by "--split/-s", and optionally "--format/-f".')
        sys.exit(0)

    elif len(sys.argv) == 3 and (sys.argv[1] == '--info' or sys.argv[1] == '-i') and sys.argv[2] == 'shape':
        print('Option "--info/-i shape" must be accompanied by "--split/-s"')
        sys.exit(0)

    args = parser.parse_args()

    out_manager = OutputManager(f'{args.output}-{args.split}-{args.info}.{args.format}' if args.output != '-' else args.output)
    out_manager2 = OutputManager([f'{args.output}-cv-{args.split}-train-{args.info}.{args.format}' if args.output != '-' else args.output,
                                  f'{args.output}-cv-{args.split}-valid-{args.info}.{args.format}' if args.output != '-' else args.output])

    form = True if args.format == 'fasta'  else False

    if args.scls:
        out_manager_scl = OutputManager(
            f'{args.output}-targets-{args.scls}.txt' if args.output != '-' else args.output)
        scls = load().scl.drop_duplicates()
        if args.scls == 'long':
            scl = scls
        elif args.scls == 'short':
            scl =scls.replace(label_abbr_dict)
        elif args.scls == 'full':
            scl = scls + ' (' + scls.replace(label_abbr_dict) + ')'

        joiner = '\n'
        output(out_manager_scl, f'SCL2205 Target Classes:\n\n{joiner.join(scl)}')
    elif args.split and args.info is None:
        if args.split not in ('0', '1', '2', '3', '4'):
            print(f'SCL2205 {args.split.capitalize()}:\n\n')
            output(out_manager, load(args.split, form), args.format)
        else:
            print(f'SCL2205 Fold-{args.split} Train-Valid:\n\n')
            # output(out_manager2, (load(args.split, form)[0], load(args.split, form)[1]), args.format)
            head_out1 = load(args.split, form)[0] #if args.format == 'fasta' else load(args.split, form)[0]
            head_out2 = load(args.split, form)[1] #if args.format == 'fasta' else load(args.split, form)[1]
            output(out_manager2, (head_out1, head_out2), args.format)
    elif args.info == 'struct':
        output(out_manager,splits_str)
        # if args.split not in ('0', '1', '2', '3', '4'):
        #     print(f'SCL2205 {args.split.capitalize()}:\n\n')
        #     output(out_manager, load(args.split, form), args.format)
        # else:
        #     print(f'SCL2205 Fold-{args.split} Train-Valid:\n\n')
        #     output(out_manager2, (load(args.split, form)[0], load(args.split, form)[1]), args.format)
    elif args.info == 'head' and args.split:
        if args.split not in ('0', '1', '2', '3', '4'):
            print(f'SCL2205 {args.split.capitalize()} (Head):\n\n')
            head_out = StringIO(''.join(map(str,load(args.split, form).readlines()[:20]))) if args.format == 'fasta'  else load(args.split).head()
            output(out_manager, head_out , args.format)
        else:
            print(f'SCL2205 Fold-{args.split} Train-Valid (Head):\n\n')
            head_out1 = StringIO(''.join(map(str,load(args.split, form)[0].readlines()[:20]))) if args.format == 'fasta'  else load(args.split)[0].head()
            head_out2 = StringIO(''.join(map(str,load(args.split, form)[1].readlines()[:20]))) if args.format == 'fasta'  else load(args.split)[1].head()
            output(out_manager2, (head_out1, head_out2), args.format)
    elif args.info == 'shape' and args.split:
        if args.split not in ('0', '1', '2', '3', '4'):
            output(out_manager,f'SCL2205 {args.split.capitalize()} Shape:\n{load(args.split).shape}\n\n')
        else:
            output(out_manager, f'SCL2205 Fold-{args.split} Train Shape:\n{load(args.split)[0].shape}\n')
            output(out_manager, f'SCL2205 Fold-{args.split} Valid Shape:\n{load(args.split)[1].shape}\n')

if __name__ == '__main__':
    main()

