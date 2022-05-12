""" """

from hal.param import Param

# number of values of each parameter to read (TODO work in progress)
NVALS = 10

# dilution fridge flange temperatures

MXC_FLANGE_TEMP = Param(
    name="MXC flange",
    filename="CH6 T ",
    pos=2,
    nvals=NVALS,
    units="K",
    uformats={"mK": range(-3, 0)},
)

STILL_FLANGE_TEMP = Param(
    name="Still flange",
    filename="CH5 T ",
    pos=2,
    nvals=NVALS,
    units="K",
    uformats={"mK": range(-3, 0)},
)

FOURK_FLANGE_TEMP = Param(
    name="4K flange",
    filename="CH2 T ",
    pos=2,
    nvals=NVALS,
    units="K",
)

FIFTYK_FLANGE_TEMP = Param(
    name="50K flange",
    filename="CH1 T ",
    pos=2,
    nvals=NVALS,
    units="K",
)

# maxigauge pressures

P1_OVC_PRES = Param(
    name="P1 OVC",
    filename="maxigauge ",
    pos=5,
    nvals=NVALS,
    units="mbar",
    scinot=True,
)

P2_STILL_PRES = Param(
    name="P2 still",
    filename="maxigauge ",
    pos=11,
    nvals=NVALS,
    units="mbar",
    scinot=True,
)

P3_COND_PRES = Param(
    name="P3 cond",
    filename="maxigauge ",
    pos=17,
    nvals=NVALS,
    units="mbar",
    ndp=0,
)

P4_COND_PRES = Param(
    name="P4 cond",
    filename="maxigauge ",
    pos=23,
    nvals=NVALS,
    units="mbar",
    ndp=0,
)

P5_TANK_PRES = Param(
    name="P5 tank",
    filename="maxigauge ",
    pos=29,
    nvals=NVALS,
    units="mbar",
    ndp=0,
)

P6_SERVICE_PRES = Param(
    name="P6 service",
    filename="maxigauge ",
    pos=35,
    nvals=NVALS,
    units="mbar",
)

# compressed air pressure
AIR_PRES = Param(
    name="Air pres",
    filename="ESP32 ",
    pos=3,
    nvals=NVALS,
    units="bar",
    bounds=(7, 10),
)

# cooling water

WATER_FLOW = Param(
    name="Water flow",
    filename="ESP32 ",
    pos=2,
    nvals=NVALS,
    units="L/min",
    ndp=0,
    bounds=(10, 25),
)

WATER_IN_TEMP = Param(
    name="Water in",
    filename="Status_",
    pos=27,
    nvals=NVALS,
    units="°C",
    ndp=1,
    bounds=(13, 23),
)

WATER_OUT_TEMP = Param(
    name="Water out",
    filename="Status_",
    pos=29,
    nvals=NVALS,
    units="°C",
    ndp=1,
    bounds=(13, 33),
)

# compressor status

OIL_TEMP = Param(
    name="Oil temp",
    filename="Status_",
    pos=31,
    nvals=NVALS,
    units="°C",
    ndp=1,
)

HELIUM_TEMP = Param(
    name="He temp",
    filename="Status_",
    pos=33,
    nvals=NVALS,
    units="°C",
    ndp=1,
)

HELIUM_HIGH_PRES = Param(
    name="He high pres",
    filename="Status_",
    pos=41,
    nvals=NVALS,
    units="psi",
    ndp=0,
)

HELIUM_LOW_PRES = Param(
    name="He low pres",
    filename="Status_",
    pos=37,
    nvals=NVALS,
    units="psi",
    ndp=0,
)


COMP_CURRENT = Param(
    name="Comp current",
    filename="Status_",
    pos=45,
    nvals=NVALS,
    units="A",
    ndp=1,
)

# flowmeter

HE_FLOW = Param(
    name="He flow",
    filename="Flowmeter ",
    pos=2,
    nvals=NVALS,
    units="mmol/s",
)

# heaters

MXC_HEATER_POWER = Param(
    name="MXC heater",
    filename="Heaters ",
    pos=3,
    nvals=NVALS,
    units="W",
    ndp=1,
    uformats={"µW": range(-8, -3)},
)

STILL_HEATER_POWER = Param(
    name="Still heater",
    filename="Heaters ",
    pos=5,
    nvals=NVALS,
    units="W",
    ndp=1,
    uformats={"mW": range(-5, 0)},
)

# collect all params in one list
CONFIG = [
    MXC_FLANGE_TEMP,
    STILL_FLANGE_TEMP,
    FOURK_FLANGE_TEMP,
    FIFTYK_FLANGE_TEMP,
    P1_OVC_PRES,
    P2_STILL_PRES,
    P3_COND_PRES,
    P4_COND_PRES,
    P5_TANK_PRES,
    P6_SERVICE_PRES,
    AIR_PRES,
    WATER_FLOW,
    WATER_IN_TEMP,
    WATER_OUT_TEMP,
    OIL_TEMP,
    HELIUM_TEMP,
    HELIUM_HIGH_PRES,
    HELIUM_LOW_PRES,
    COMP_CURRENT,
    HE_FLOW,
    MXC_HEATER_POWER,
    STILL_HEATER_POWER,
]
