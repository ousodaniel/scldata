import pandas as pd
from io import StringIO
from typing import TextIO, Optional


def seq_df_to_fasta_handle(df: pd.DataFrame, header_col: Optional[str]=None, description_col: Optional[str]=None, seq_col: str= 'seq') -> TextIO:
    '''
    Convert a pandas sequence DataFrame to a FASTA-formatted StringIO handle.

    Params:
        df Sequence DataFrame.
        identifier_col Name of column to use as the fasta sequence header if not index/None. By default, the index is the header. All spaces are replaced with underscores.
        description_col Name of column to use for sequence description, if 'description_col' is not None. By default, no description is used.
        seq_col Column for the sequence data.

    Returns:
        StringIO handle.
    '''
    fasta_io = StringIO()

    header_col = header_col.strip() if header_col else None
    description_col = description_col.strip() if description_col else None

    # Format: >header desc\nseq\n
    fasta_data = (
            '>' + df.index.astype(str).str.strip().replace(r' +', '_', regex=True) if header_col is None else df[header_col].astype(str).str.strip().replace(r' +', '_', regex=True) +
            f' {df[description_col].astype(str).str.strip() if description_col is None else ""}' +
            '\n' + df[seq_col.strip()].astype(str).str.strip().upper() +
            '\n'
    )

    # Combine all rows into a single string and write to buffer
    fasta_io.write(''.join(fasta_data))

    # Reset pointer to the beginning for the caller to read
    fasta_io.seek(0)

    return fasta_io


if __name__ == "__main__":
    # Quick example usage
    data = {
        'scl': ['Cytoplasm', 'Nucleus'],
        'seq': ['MAGA', 'MTYPR']
    }
    test_df = pd.DataFrame(data, index=['prot_1', 'prot_2'])

    handle = seq_df_to_fasta_handle(test_df)
    print(handle.read())
