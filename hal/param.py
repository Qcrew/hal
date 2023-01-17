""" """

import math

import pint


class Param:
    """ """

    def __init__(
        self,
        name: str,
        filename: str,
        pos: int | str,
        category: str,
        nvals: int = 1,
    ) -> None:
        """
        name (str) displayed name of this param
        filename (str) prefix of the log file this param is logged in (include any leading or trailing spaces)
        pos (int) indexed position of the param in the log file (follow 0-indexing) or (str) keyword name of the parameter as logged in the log file (value is assumed to be adjacent to keyword index in logs)
        category (str) category this param belongs to (to enable easy filtering on Notion database)
        nvals (int) number of latest values (from the end of the log file) to read, default = 1.
        """
        self.name = name
        self.filename = filename
        self.pos = pos
        self.category = category
        self.nvals = nvals

    def __repr__(self) -> str:
        """ """
        return f"{self.__class__.__name__}({self.name})"

    def parse(self, value: str) -> str:
        """ """
        raise NotImplementedError("Subclass(es) to implement parse()")

    def validate(self, value: str) -> bool:
        """ """
        raise NotImplementedError("Subclass(es) to implement validate()")


class BinParam(Param):
    """binary parameter that takes on two values - 0 (TRUE) and 1 (FALSE)"""

    def parse(self, value: str) -> str:
        """ """
        return str(bool(value))

    def validate(self, value: str) -> bool:
        """ """
        return int(float(value)) in (0, 1)


class NumParam(Param):
    """numerical parameter that takes on real number values with the option of attaching physical units"""

    ureg = pint.UnitRegistry()

    def __init__(
        self,
        units: str,
        ndp: int = 2,
        uformats: dict[str, range] = None,
        has_scinot: bool = False,
        bounds: tuple[float, float] = None,
        **kwargs,
    ) -> None:
        """
        units (str) string indicating the units the Param value is logged in. string must be recognized by Pint.
        ndp (int) number of decimal places to round the value(s) to, default = 2.
        uformats (dict) additional unit formatting for the value to be displayed in human readable format. Key = units (string must be recognized by Pint) and value = range object, then the unit will be applied based on which range the order of magnitude of the value falls in.
        scinot (bool) whether or not to display the number in scientific notation
        bounds (float, float) tuple (min, max) indicate the open interval of non-alarming values for this parameter
        """
        self.units = getattr(NumParam.ureg, str(units), None)  # None = dimensionless
        self.ndp = ndp
        self.uformats = uformats
        self.has_scinot = has_scinot
        self.bounds = bounds
        super().__init__(**kwargs)

    def parse(self, value: str) -> str:
        """
        value (str) raw value string to be parsed, must be compatible with being casted as a float.
        return parsed value string to be displayed to user
        """
        quantity = NumParam.ureg.Quantity(float(value), self.units)

        if self.uformats and quantity.magnitude:  # ignore zero values
            exponent = math.floor(math.log10(abs(float(value))))
            for units, interval in self.uformats.items():
                if exponent in interval:
                    quantity = quantity.to(units)
                    break

        if self.has_scinot:
            return f"{quantity:~.{self.ndp}e}"
        else:
            return f"{quantity:~.{self.ndp}f}"

    def validate(self, value: str) -> bool:
        """check if value (str), which should be castable to float, is within bounds, if bounds have been defined
        return bool indicating whether the value is valid or not
        """
        quantity = pint.Quantity(*value.split(maxsplit=1))
        magnitude = float(quantity.magnitude)
        if self.bounds and not self.bounds[0] < magnitude < self.bounds[1]:
            return False
        return True
