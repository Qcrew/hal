""" This module contains utilities that read data logged by instruments """

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import time

import numpy as np

from hal.logger import logger
from hal.param import Param


class LogReader:
    """reads a list of params from their log file"""

    def __init__(self, path: Path, *params: Param, split: str = ",") -> None:
        """
        path (Path) path to the main logs folder
        params (Param) a sequence of Params to be read from their log file
        split: (str) string used to split the entries in each line of the log file
        """
        self.path = path
        self.params = params
        self.split = split
        self._date = self.date
        self._logfiles = self.logfiles
        logger.debug(f"Ready to read {len(params)} params from {path = }.")

    @property
    def date(self) -> str:
        """return current date string in yy:mm:dd format"""
        return datetime.now().strftime("%y-%m-%d")

    @property
    def logfiles(self) -> dict[Path, list[Param]]:
        """return dict of logfile Paths mapped to a list of Params logged in them"""
        logfiles = defaultdict(list)
        filepaths = {param: self.locate(param) for param in self.params}
        for param, filepath in filepaths.items():
            logfiles[filepath].append(param)
        return logfiles

    def locate(self, param: Param) -> Path:
        """
        param (Param) the param to locate, based on its 'filename' attribute
        return Path to log file generated based on Bluefors' log file naming convention
        """
        date = self.date
        return self.path / f"{date}/{param.filename}{date}.log"

    def _check_logfile_rotation(self) -> None:
        """ """
        date = self.date  # get current date
        if date != self._date:  # account for Bluefors' log rotation
            self._logfiles = self.logfiles
            self._date = date
            logger.debug("Rotated log files!")

    def read(self) -> dict[Param, tuple[np.ndarray, np.ndarray]]:
        """
        return dict[str, tuple[np.ndarray, np.ndarray]] with key = Param object and value = two 1D np arrays of strings, first array contains timestamps in mm-dd hh:mm format, second array contains raw param string values. length of each array equals the param's 'nvals' attribute. value is (None, None) if path doesn't exist.
        assume col = 1 is for timestamp
        """
        self._check_logfile_rotation()  # ensure correct logfiles are being read from

        data = {}
        for path, params in self._logfiles.items():
            if not path.exists():
                for param in params:
                    data[param] = (None, None)
            else:
                cols = (1, *(p.pos for p in params))  # col=1 is for timestamp
                txt = self.loadtxt(path, cols)

                for idx, param in enumerate(params, start=1):
                    timestamps = txt[0][-param.nvals :]
                    values = txt[idx][-param.nvals :]
                    data[param] = (timestamps, values)

        return data

    def loadtxt(self, path, cols, wait=10) -> np.ndarray:
        """re-implementation of numpy's loadtxt method customised for LogReader"""
        try:
            txt = np.loadtxt(path, dtype=str, delimiter=self.split, usecols=cols).T
        except IndexError:  # when Bluefors log format is inconsistent
            logger.debug(f"Bad log format, removing last line of {path}...")
            time.sleep(wait)
            remove_last_line(path)
            time.sleep(wait)
            self.loadtxt(path, cols)  # recursive call to handle multiple bad log lines
        else:
            return txt


def remove_last_line(path) -> None:
    """Remove the last line of the file at the given path"""
    with open(path, "r+") as logfile:
        curr_pos = prev_pos = logfile.tell()
        while logfile.readline():
            prev_pos = curr_pos
            curr_pos = logfile.tell()
        logfile.truncate(prev_pos)
