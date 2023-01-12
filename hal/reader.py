""" This module contains utilities that read data logged by instruments """

from collections import defaultdict
from datetime import datetime
from pathlib import Path

from hal.param import Param


class Reader:
    """ """

    def __init__(self, path: str, *params: Param) -> None:
        """
        path (str) path to the main logs folder
        params (Param) a sequence of Params to be read from their log file
        """
        self.path: Path = Path(path)
        self.params: tuple[Param] = params
        self.delimiter: str = ","

    @property
    def logspec(self) -> dict[Path, list[Param]]:
        """return dict of logfile Paths mapped to a list of Params logged in them"""
        # get current date in yy-mm-dd format e.g. 23-01-12
        date = datetime.now().strftime("%y-%m-%d")
        # get dict with key = Param and value = logfile Path
        fpaths = {p: self.path / f"{date}/{p.filename}{date}.log" for p in self.params}
        # return dict with key = logfile Path and value = list[Param]
        logspec = defaultdict(list)
        for param, filepath in fpaths.items():
            logspec[filepath].append(param)
        return logspec

    def read(self) -> dict[Param, dict[str, str]]:
        """
        Read logfiles for all Params in config and return a data dictionary
        Method is purposely written in a naive inefficient way to avoid reading inconsistently logged data
        return dict with key = Param object, value = dict with key = timestamp string and value = param value string. number of entries in dictionary = param.nval and insertion order is reverse chronological. value is None if path to Param's logfile does not exist.
        assume:
            the second entry (index = 1) of each line in log file is the time stamp
            the terminating character for each line is "/n" and delimiter is ","
        """
        data = {param: {} for param in self.params}
        for path, params in self.logspec.items():
            if path.exists():  # empty data dict if path does not exist
                with path.open() as file:
                    tokens = [line.rstrip("\n").split(",") for line in file.readlines()]
                keys = [param.key for param in params if param.key]
                for param in params:  # read 'nvals' latest tokens for each param
                    for token in tokens[-param.nvals:][::-1]:
                        if all(key in token for key in keys): # ignore bad tokens
                            data[param][token[1]] = token[param.pos]  # token[1] = time
        return data
