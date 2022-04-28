""" This module contains utilities that read data logged by instruments """

from pathlib import Path

from hal.logger import logger

""" logspec is a dict that maps the log file names (only the prefix, excluding the date suffix) to the names of the parameters logged in them. the tuples below have been constructed after inspecting the log files. """
LOGSPEC = {
    "CH1 T": ("Date", "Time", "50K flange [K]"),
    "CH2 T": ("Date", "Time", "4K flange [K]"),
    "CH5 T": ("Date", "Time", "Still flange [K]"),
    "CH6 T": ("Date", "Time", "MXC flange [K]"),
    "Heaters": ("Date", "Time", "MXC heater [W]", "Still heater [W]"),
    "Flowmeter": ("Date", "Time", "Mix flow [mmol/s]"),
    "maxigauge": (
        "Date",
        "Time",
        *(None,) * 3,
        "P1 OVC [mbar]",
        *(None,) * 5,
        "P2 still [mbar]",
        *(None,) * 5,
        "P3 cond [mbar]",
        *(None,) * 5,
        "P4 cond [mbar]",
        *(None,) * 5,
        "P5 tank [mbar]",
        *(None,) * 5,
        "P6 service [mbar]",
        *(None,) * 3,
    ),
    "Status": (
        "Date",
        "Time",
        *(None,) * 25,
        "Water temp in [°C]",
        None,
        "Water temp out [°C]",
        None,
        "Oil temp [°C]",
        None,
        "Helium temp [°C]",
        *(None,) * 3,
        "Helium pres low [psi]",
        *(None,) * 3,
        "Helium pres high [psi]",
        *(None,) * 3,
        "Comp current [A]",
        *(None,) * 30,
    ),
}

""" Ignore the last <PADDING> characters of each log file - these characters are a space followed by a date string 'yy-mm-dd' i.e. 9 characters in all. The logspec keys are the other characters in the log file name they except these last 9"""
PADDING = 9


class LogManager:
    """Manages multiple log readers, each of which reads data from one log file. Sets the log file for these readers based on the specified file name format and file rotation time. Collects data from all readers it is managing into one dictionary ('data' attribute)."""

    def __init__(self, path: Path) -> None:
        """path: (Path) path to folder containing log files"""
        logger.debug(f"Initializing a log manager at {path = }...")

        self._path = path
        self._logfiles = [file for file in path.iterdir() if file.suffix == ".log"]
        logger.debug(f"Found logfiles: {[str(file) for file in self._logfiles]}.")

        self._readers = None
        self._initialize_readers()

    def _initialize_readers(self) -> None:
        """ """
        readers: dict[str, LogReader] = {}
        for file in self._logfiles:
            name = file.stem[:-PADDING]
            if name in LOGSPEC.keys():  # we want to log the data in this file
                readers[name] = LogReader(file, *LOGSPEC[name])
                logger.debug(f"Prepared to log data from '{file.stem}'!")
        self._readers = readers

    @property
    def data(self) -> dict[str, str]:
        """return dict of dicts"""
        data = {}
        for name, reader in self._readers.items():
            data[name] = reader.data
        return data

class LogReader:
    """A generic log reader that reads the last line from a given log file, splits the line with a given delimiter, and maps each value to a corresponding key from a given tuple of keys. Values in the log file can be ignored by setting their corresponding key = None."""

    def __init__(self, path: Path, *keys: str, delimiter: str = ",") -> None:
        """path: (Path) path to the log file
        keys: (str) ordered names that correspond to the values read from the log file. pass key = None to ignore the value entirely.
        delimiter: (str) string used to split the entries in the line, default = ","
        """
        self._path = path
        self._keys = keys
        self._delimiter = delimiter

    @property
    def data(self) -> dict[str, str]:
        """property that extracts parameter names and values from the final line of the log file (which contains the latest parameter value(s)).
        returns dict[str, str] with key = parameter name and value = parameter value
        """
        with self._path.open() as log:
            line = log.readlines()[-1]
            values = line.strip().split(self._delimiter)
            return {k: v for k, v in zip(self._keys, values) if k is not None}
