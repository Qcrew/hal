""" This module contains utilities that read data logged by instruments """

from pathlib import Path

from hal.logger import logger

""" logspec is a dict that maps the log file names (only the prefix, excluding the date suffix) to the names of the parameters logged in them. the tuples below have been constructed after inspecting the log files. the params are displayed on the notion in the same order, so the notion page structure must be set accordingly. """
LOGSPEC = {
    "CH6 T": ("Date", "Time", "MXC flange"),
    "CH5 T": ("Date", "Time", "Still flange"),
    "CH2 T": ("Date", "Time", "4K flange"),
    "CH1 T": ("Date", "Time", "50K flange"),
    "maxigauge": (
        "Date",
        "Time",
        *(None,) * 3,
        "P1 OVC",
        *(None,) * 5,
        "P2 still",
        *(None,) * 5,
        "P3 cond",
        *(None,) * 5,
        "P4 cond",
        *(None,) * 5,
        "P5 tank",
        *(None,) * 5,
        "P6 service",
        *(None,) * 3,
    ),
    "Flowmeter": ("Date", "Time", "Mix flow"),
    "Heaters": ("Date", "Time", "MXC heater", "Still heater"),
    "Status": (
        "Date",
        "Time",
        *(None,) * 25,
        "Water temp in",
        None,
        "Water temp out",
        None,
        "Oil temp",
        None,
        "Helium temp",
        *(None,) * 3,
        "Helium pres low",
        *(None,) * 3,
        "Helium pres high",
        *(None,) * 3,
        "Comp current",
        *(None,) * 30,
    ),
}

""" How each param will be parsed """
PARSESPEC = {
    "MXC flange": lambda v: f"{float(v) * 1e3:.2e} mK",
    "Still flange": lambda v: f"{float(v):.2e} K",
    "4K flange": lambda v: f"{round(float(v), 2)} K",
    "50K flange": lambda v: f"{round(float(v), 2)} K",
    "P1 OVC": lambda v: f"{float(v):.2e} mbar",
    "P2 still": lambda v: f"{float(v):.2e} mbar",
    "P3 cond": lambda v: f"{float(v):.2e} mbar",
    "P4 cond": lambda v: f"{float(v):.2e} mbar",
    "P5 tank": lambda v: f"{float(v):.2e} mbar",
    "P6 service": lambda v: f"{float(v):.2e} mbar",
    "Mix flow": lambda v: f"{round(float(v), 2)} mmol/s",
    "MXC heater": lambda v: f"{float(v) * 1e6:.2e} μW",
    "Still heater": lambda v: f"{float(v) * 1e3:.2e} mW",
    "Water temp in": lambda v: f"{round(float(v), 2)} °C",
    "Water temp out": lambda v: f"{round(float(v), 2)} °C",
    "Oil temp": lambda v: f"{round(float(v), 2)} °C",
    "Helium temp": lambda v: f"{round(float(v), 2)} °C",
    "Helium pres low": lambda v: f"{float(v):.2} psi",
    "Helium pres high": lambda v: f"{float(v):.2} psi",
    "Comp current": lambda v: f"{round(float(v), 2)} A",
}


class LogManager:
    """Manages multiple log readers, each of which reads data from one log file. Sets the log file for these readers based on the specified file name format and file rotation time. Collects data from all readers it is managing into one dictionary ('data' attribute)."""

    def __init__(self, path: Path) -> None:
        """path: (Path) path to folder containing log files"""
        logger.debug(f"Initializing a log manager at {path = }...")

        self._readers: dict[str, LogReader] = {}

        logfiles = [file for file in path.iterdir() if file.suffix == ".log"]
        for key in LOGSPEC.keys():  # we want to follow LOGSPEC key order
            for file in logfiles:
                if key in file.stem:  # we want to log the data in this file
                    self._readers[key] = LogReader(file, *LOGSPEC[key])
                    logger.debug(f"Prepared to log data from '{file.name}'!")

        self._parser = LogParser()

    @property
    def data(self):
        """return list of dicts"""
        data = {name: reader.data for name, reader in self._readers.items()}
        return self._parser.parse(data)


class LogParser:
    """ """

    def parse(self, data: dict[str, dict[str, str]]) -> list[dict[str, str]]:
        """ """
        pdata = {}  # p means parsed
        for key, names in LOGSPEC.items():
            if key in data.keys():
                # guaranteed that each data dict contains two keys "Date" and "Time"
                date, time = data[key].pop("Date"), data[key].pop("Time")
                pdata[key] = {k: PARSESPEC[k](v) for k, v in data[key].items()}
                pdata[key]["Timestamp"] = f"{date} {time}"
            else:
                pdata[key] = {k: "N/A" for k in names if k not in ("Date", "Time")}
                pdata[key]["Timestamp"] = "N/A"
        return list(pdata.values())


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
