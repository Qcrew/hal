""" """

import math

import pint


class Param:
    """ """

    ureg = pint.UnitRegistry()

    def __init__(
        self,
        name: str,
        filename: str,
        pos: int,
        nvals: int,
        units: str,
        ndp: int = 2,
        uformats: dict[str, range] = None,
        scinot: bool = False,
        bounds: tuple[float, float] = None,
    ) -> None:
        """
        name (str) displayed name of this param
        filename (str) prefix of log file (include any leading or trailing spaces)
        pos (int) indexed position of the param in the log file (follow 0-indexing)
        nvals (int) number of latest values (from the end of the log file) to read
        units (str | dict) string indicating the units the Param value is logged in. string must be recognized by Pint.
        ndp (int) number of decimal places to round the value(s) to, default = 2.
        uformats (dict) additional unit formatting for the value to be displayed in human readable format. Key = units (string must be recognized by Pint) and value = range object, then the unit will be applied based on which range the order of magnitude of the value falls in.
        scinot (bool) whether or not to display the number in scientific notation
        bounds (float, float) tuple (min, max) indicate the open interval of non-alarming values for this parameter
        """
        self.name = name
        self.filename = filename
        self.pos = pos
        self.nvals = nvals
        self.units = getattr(Param.ureg, str(units), None)  # None means dimensionless
        self.ndp = ndp
        self.uformats = uformats
        self.scinot = scinot
        self.bounds = bounds

    def __repr__(self) -> str:
        """ """
        return f"{self.__class__.__name__}({self.name})"

    def parse(self, value: str) -> str:
        """
        value (str) raw value string to be parsed, must be compatible with being casted as a float.
        return parsed value string to be displayed to user
        """
        quantity = Param.ureg.Quantity(float(value), self.units)

        if self.uformats and quantity.magnitude:  # ignore zero values
            exponent = math.floor(math.log10(abs(float(value))))
            for units, interval in self.uformats.items():
                if exponent in interval:
                    quantity = quantity.to(units)
                    break

        if self.scinot:
            return f"{quantity:~.{self.ndp}e}"
        else:
            return f"{quantity:~.{self.ndp}f}"

    def validate(self, value: str) -> bool:
        """ check if value (str), which should be castable to float, is within bounds, if bounds have been defined
        return bool indicating whether the value is valid or not
        """
        if self.bounds and not self.bounds[0] < float(value) < self.bounds[1]:
            return False
        return True
