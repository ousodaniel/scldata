import sys
from typing import List, Union, TextIO, Sequence


class OutputManager:
    """
    Manages one or more output handles (stdout or files).
    """

    def __init__(self, paths: Union[str, Sequence[str]]):
        """
            Init handles for stdout or files.

            Parameters
            ----------
            `paths`: `str` | `Sequence[str]`

            :param: paths: `str` | `Sequence[str]`, Path to output file(s).

            Returns
            -------
            `self`

            :return: Class instance

            """
        self.paths = [paths] if isinstance(paths, str) else paths
        self.handles: List[TextIO] = []

    def __repr__(self) -> str:
        # Returns a string like: OutputManager(paths=['-', 'results.fasta'])
        return f'{self.__class__.__name__}(paths={self.paths!r})'

    def __len__(self) -> int:
        """Returns the number of paths this manager is responsible for."""
        return len(self.paths)

    @property
    def count(self) -> int:
        """Getter for the number of handles managed by this instance."""
        return len(self.paths)

    def __enter__(self) -> Union[TextIO, List[TextIO]]:
        """Opens all paths and returns a single handle or a list of handles."""
        # Clear handles in case the same instance is used twice
        self.handles = []

        for path in self.paths:
            if path == '-':
                self.handles.append(sys.stdout)
            else:
                self.handles.append(open(path, 'w', encoding='utf-8'))

        return self.handles[0] if len(self.handles) == 1 else self.handles

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures all file handles are closed, but skips stdout."""
        for handle in self.handles:
            if handle is not sys.stdout:
                handle.close()
