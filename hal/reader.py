""" This module contains utilities that read data logged by instruments """

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import time

from hal.config import LOGFOLDER, PARAMS
from hal.param import Param


class Reader:
    """ """

    def __init__(self) -> None:
        """ """
        self._path: Path = Path(LOGFOLDER)
        self._params: tuple[Param] = PARAMS
        self._data: dict[Param, dict[str, str]] = self._read(last=False)

    @property
    def logspec(self) -> dict[Path, list[Param]]:
        """return dict of logfile Paths mapped to a list of Params logged in them"""
        # get current date in yy-mm-dd format e.g. 23-01-12
        date = datetime.now().strftime("%y-%m-%d")
        # get dict with key = Param and value = logfile Path
        paths = {p: self._path / f"{date}/{p.filename}{date}.log" for p in self._params}
        # return dict with key = logfile Path and value = list[Param]
        logspec = defaultdict(list)
        for param, filepath in paths.items():
            logspec[filepath].append(param)
        return logspec

    def _read(self, last=True) -> dict[Param, dict[str, str]]:
        """
        Internal method to read logfiles. If last=True, data dictionary value contains only the last timestamp and value pair, if last=False, we read last 'param.nvals' in reverse chronological order for each Param.
        return dict with same structure as read() and make same assumptions as read()
        """
        data = {param: {} for param in self._params}
        for path, params in self.logspec.items():
            if path.exists():  # empty data dict if path does not exist
                with path.open() as file:
                    tokens = [line.rstrip("\n").split(",") for line in file.readlines()]
                for param in params:  # read 'nvals' or latest token(s) for each param
                    nvals = 1 if last else param.nvals
                    for token in tokens[-nvals:][::-1]:
                        timestamp = f"{token[0]} {token[1]}"
                        if isinstance(param.pos, int):  # pos = col index
                            data[param][timestamp] = token[param.pos]
                        elif isinstance(param.pos, str):  # pos = keyword adjacent
                            try:
                                idx = token.index(param.pos)
                            except ValueError:  # keyword not present in token = bad log
                                pass  # ignore bad log
                            else:  # assume value is right next to position keyword
                                data[param][timestamp] = token[idx + 1]
        return data

    def read(self) -> dict[Param, dict[str, str]]:
        """
        Read logfiles for all Params and return a data dictionary containing 'param.nvals' latest timestamps and values for each Param
        Method is purposely written in a naive inefficient way to avoid reading inconsistently logged data
        return Data dictionary with key = Param, value = dict with key = timestamp string and value = Param value string. number of entries in dictionary = param.nval and insertion order is reverse chronological. Data dictionary value is empty if path to Param's logfile does not exist.
        assume:
            the 1st & 2nd entries of each line in log file consist of the time stamp
            the terminating character for each line is "/n" and delimiter is ","
        """
        new_data = self._read()
        for param, datadict in self._data.items():
            num_entries = len(datadict)
            datadict |= new_data[param]  # update data dict with new data
            diff_entries = len(datadict) - num_entries
            if num_entries:  # don't remove elements if datadict is initially empty
                for _ in range(diff_entries):  # remove earliest elements
                    del datadict[next(iter(datadict))]
        data = {param: datadict.copy() for param, datadict in self._data.items()}
        return data  # don't return self._data, return copy instead
