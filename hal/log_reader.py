""" This module contains utilities that parse data logged by instruments """

from pathlib import Path



class LogReader:
    """ A generic log reader that reads the last line from a given log file, splits the line with a given delimiter, and maps each value to a corresponding key from a given tuple of keys. Values in the log file can be ignored by setting their corresponding key = None.
    """

    def __init__(self, path: Path, *keys: str, delimiter: str = ",") -> None:
        """ path: (Path) path to the log file
            keys: (str) ordered names that correspond to the values read from the log file. pass key = None to ignore the value entirely.
            delimiter: (str) string used to split the entries in the line, default = ","
        """
        self._path = path
        self._keys = keys
        self._delimiter = delimiter

    @property
    def data(self) -> dict[str, str]:
        """ property that extracts parameter names and values from the final line of the log file (which contains the latest parameter value(s)).
        returns dict[str, str] with key = parameter name and value = parameter value
        """
        with self._path.open() as log:
            line = log.readlines()[-1]
            values = line.strip().split(self._delimiter)
            return {k: v for k, v in zip(self._keys, values) if k is not None}

    @property
    def path(self) -> Path:
        """ """
        return self._path

    @path.setter
    def path(self, value: Path) -> None:
        """ """
        self._path = value

if __name__ == "__main__":
    params = ("Date", "Time", "Flow")
    path = Path("C:/Users/athar/Desktop/Flowmeter 22-04-27.log")
    lr = LogReader(path, *params)
    print(lr.data)
