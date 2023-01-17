""" Runtime and Parameter configuration for HAL """

from pathlib import Path

from hal.param import BinParam, Param, NumParam


# Runtime settings

# name of the dilution fridge whose parameters are being monitored
FRIDGE_NAME = "Merlin"

# path to the main logs folder
LOGFOLDER = "C:/Users/Qcrew4/Bluefors logs"

# sleep time between two successive read-post cycles
INTERVAL = 1  # seconds

# delay between successive Notion API calls
DELAY = 0.1  # seconds

# a txt file must be at this path and contain one value - HAL's Notion integration token
NOTION_TOKENPATH = Path.cwd() / "notion_token.txt"

# a txt file must be at this path and contain two comma separated values in this format:
# <HAL's Slack token>,<#hal-alerts channel ID>
SLACK_TOKENPATH = Path.cwd() / "slack_token.txt"


# Parameter settings

# dilution fridge flange temperatures

MXC_FLANGE_TEMP = NumParam(
    name="MXC flange temp",
    filename="CH6 T ",
    pos=2,
    category="Temperatures",
    units="K",
    uformats={"mK": range(-3, 0)},
)

STILL_FLANGE_TEMP = NumParam(
    name="Still flange temp",
    filename="CH5 T ",
    pos=2,
    category="Temperatures",
    units="K",
    uformats={"mK": range(-3, 0)},
)

FOURK_FLANGE_TEMP = NumParam(
    name="4K flange temp",
    filename="CH2 T ",
    pos=2,
    category="Temperatures",
    units="K",
)

FIFTYK_FLANGE_TEMP = NumParam(
    name="50K flange temp",
    filename="CH1 T ",
    pos=2,
    category="Temperatures",
    units="K",
)

# maxigauge pressures

P1_OVC_ON = BinParam(name="P1 on", filename="maxigauge ", pos=4, category="Pressures")

P1_OVC_PRES = NumParam(
    name="P1 OVC",
    filename="maxigauge ",
    pos=5,
    category="Pressures",
    units="mbar",
    has_scinot=True,
)

P2_STILL_ON = BinParam(
    name="P2 on", filename="maxigauge ", pos=10, category="Pressures"
)

P2_STILL_PRES = NumParam(
    name="P2 still",
    filename="maxigauge ",
    pos=11,
    category="Pressures",
    units="mbar",
    has_scinot=True,
)

P3_COND_ON = BinParam(name="P3 on", filename="maxigauge ", pos=16, category="Pressures")

P3_COND_PRES = NumParam(
    name="P3 cond",
    filename="maxigauge ",
    pos=17,
    category="Pressures",
    units="mbar",
    ndp=0,
)

P4_COND_ON = BinParam(name="P4 on", filename="maxigauge ", pos=22, category="Pressures")

P4_COND_PRES = NumParam(
    name="P4 cond",
    filename="maxigauge ",
    pos=23,
    category="Pressures",
    units="mbar",
    ndp=0,
)

P5_TANK_ON = BinParam(name="P5 on", filename="maxigauge ", pos=28, category="Pressures")

P5_TANK_PRES = NumParam(
    name="P5 tank",
    filename="maxigauge ",
    pos=29,
    category="Pressures",
    units="mbar",
    ndp=0,
)

P6_SERVICE_ON = BinParam(
    name="P6 on", filename="maxigauge ", pos=34, category="Pressures"
)

P6_SERVICE_PRES = NumParam(
    name="P6 service",
    filename="maxigauge ",
    pos=35,
    category="Pressures",
    units="mbar",
)

# pumps

SCROLL1_ON = BinParam(
    name="Scroll 1 on", filename="Channels ", pos="scroll1", category="Pumps"
)

SCROLL2_ON = BinParam(
    name="Scroll 2 on", filename="Channels ", pos="scroll2", category="Pumps"
)

TURBO1_ON = BinParam(
    name="Turbo 1 on", filename="Channels ", pos="turbo1", category="Pumps"
)


SCROLL_FREQ = NumParam(
    name="Scroll rot freq",
    filename="Status_",
    pos="nxdsf",
    category="Pumps",
    units="Hz",
    ndp=1,
)

SCROLL_PUMP_TEMP = NumParam(
    name="Scroll pump temp",
    filename="Status_",
    pos="nxdspt",
    category="Pumps",
    units="K",
    uformats={"°C": range(0, 4)},
    ndp=1,
)

SCROLL_CONT_TEMP = NumParam(
    name="Scroll cont temp",
    filename="Status_",
    pos="nxdsct",
    category="Pumps",
    units="K",
    uformats={"°C": range(0, 4)},
    ndp=1,
)

TURBO_FREQ = NumParam(
    name="Turbo rot freq",
    filename="Status_",
    pos="tc400actualspd",
    category="Pumps",
    units="Hz",
    ndp=1,
)

TURBO_POW = NumParam(
    name="Turbo drv pow",
    filename="Status_",
    pos="tc400drvpower",
    category="Pumps",
    units="W",
    ndp=1,
)

TURBO_EDU_OVER_TEMP = BinParam(
    name="Is turbo EDU over temp",
    filename="Status_",
    pos="tc400ovtempelec",
    category="Pumps",
)

TURBO_PUMP_OVER_TEMP = BinParam(
    name="Is turbo pump over temp",
    filename="Status_",
    pos="tc400ovtemppum",
    category="Pumps",
)

# flows

WATER_FLOW = NumParam(
    name="Cooling water flow",
    filename="ESP32 ",
    pos=2,
    category="Flows",
    units="L/min",
    ndp=0,
    bounds=(10, 30),
)

HE_FLOW = NumParam(
    name="Helium flow",
    filename="Flowmeter ",
    pos=2,
    category="Flows",
    units="mmol/s",
)

# heaters

MXC_HEATER_ON = BinParam(
    name="MXC heater on", filename="Heaters ", pos=2, category="Heaters"
)

MXC_HEATER_POWER = NumParam(
    name="MXC heater power",
    filename="Heaters ",
    pos=3,
    category="Heaters",
    units="W",
    ndp=1,
    uformats={"µW": range(-8, -3)},
)

STILL_HEATER_ON = BinParam(
    name="Still heater on", filename="Heaters ", pos=4, category="Heaters"
)

STILL_HEATER_POWER = NumParam(
    name="Still heater power",
    filename="Heaters ",
    pos=5,
    category="Heaters",
    units="W",
    ndp=1,
    uformats={"mW": range(-5, 0)},
)

STILL_HEATSWITCH_ON = BinParam(
    name="Still heatswitch on", filename="Channels ", pos="hs-still", category="Heaters"
)

MXC_HEATSWITCH_ON = BinParam(
    name="MXC heatswitch on", filename="Channels ", pos="hs-mc", category="Heaters"
)

EXT_ON = BinParam(name="Ext on", filename="Channels ", pos="ext", category="Heaters")

# compressors

CPA_RUN = BinParam(
    name="Compressor on", filename="Status_", pos="cparun", category="Compressors"
)

PULSE_TUBE_ON = BinParam(
    name="Pulse tube on", filename="Channels ", pos="pulsetube", category="Compressors"
)

WATER_IN_TEMP = NumParam(
    name="Input cooling water temp",
    filename="Status_",
    pos="cpatempwi",
    category="Compressors",
    units="°C",
    ndp=1,
    bounds=(13, 25),
)

WATER_OUT_TEMP = NumParam(
    name="Output cooling water temp",
    filename="Status_",
    pos="cpatempwo",
    category="Compressors",
    units="°C",
    ndp=1,
    bounds=(13, 35),
)

OIL_TEMP = NumParam(
    name="Oil temp",
    filename="Status_",
    pos="cpatempo",
    category="Compressors",
    units="°C",
    ndp=1,
)

HELIUM_TEMP = NumParam(
    name="Helium temp",
    filename="Status_",
    pos="cpatemph",
    category="Compressors",
    units="°C",
    ndp=1,
)

AVG_LOW_PRES = NumParam(
    name="Helium low pres avg",
    filename="Status_",
    pos="cpalpa",
    category="Compressors",
    units="psi",
    ndp=0,
)

HELIUM_HIGH_PRES = NumParam(
    name="Helium high pres avg",
    filename="Status_",
    pos="cpahpa",
    category="Compressors",
    units="psi",
    ndp=0,
)

COMP_CURRENT = NumParam(
    name="Compressor current",
    filename="Status_",
    pos="cpacurrent",
    category="Compressors",
    units="A",
    ndp=1,
)

# valves

AIR_PRES = NumParam(
    name="Compressed air pres",
    filename="ESP32 ",
    pos=3,
    category="Valves",
    units="bar",
    bounds=(4, 8),
)

CTRL_PRES_OK = BinParam(
    name="Control pres ok", filename="Status_", pos="ctr_pressure_ok", category="Valves"
)

V1_ON = BinParam(name="V1 on", filename="Channels ", pos="v1", category="Valves")

V2_ON = BinParam(name="V2 on", filename="Channels ", pos="v2", category="Valves")

V3_ON = BinParam(name="V3 on", filename="Channels ", pos="v3", category="Valves")

V4_ON = BinParam(name="V4 on", filename="Channels ", pos="v4", category="Valves")

V5_ON = BinParam(name="V5 on", filename="Channels ", pos="v5", category="Valves")

V6_ON = BinParam(name="V6 on", filename="Channels ", pos="v6", category="Valves")

V7_ON = BinParam(name="V7 on", filename="Channels ", pos="v7", category="Valves")

V8_ON = BinParam(name="V8 on", filename="Channels ", pos="v8", category="Valves")

V9_ON = BinParam(name="V9 on", filename="Channels ", pos="v9", category="Valves")

V10_ON = BinParam(name="V10 on", filename="Channels ", pos="v10", category="Valves")

V11_ON = BinParam(name="V11 on", filename="Channels ", pos="v11", category="Valves")

V12_ON = BinParam(name="V12 on", filename="Channels ", pos="v12", category="Valves")

V13_ON = BinParam(name="V13 on", filename="Channels ", pos="v13", category="Valves")

V14_ON = BinParam(name="V14 on", filename="Channels ", pos="v14", category="Valves")

V15_ON = BinParam(name="V15 on", filename="Channels ", pos="v15", category="Valves")

V16_ON = BinParam(name="V16 on", filename="Channels ", pos="v16", category="Valves")

V17_ON = BinParam(name="V17 on", filename="Channels ", pos="v17", category="Valves")

V18_ON = BinParam(name="V18 on", filename="Channels ", pos="v18", category="Valves")

V19_ON = BinParam(name="V19 on", filename="Channels ", pos="v19", category="Valves")

V20_ON = BinParam(name="V20 on", filename="Channels ", pos="v20", category="Valves")

V21_ON = BinParam(name="V21 on", filename="Channels ", pos="v21", category="Valves")

V22_ON = BinParam(name="V22 on", filename="Channels ", pos="v22", category="Valves")

V23_ON = BinParam(name="V23 on", filename="Channels ", pos="v23", category="Valves")

# a sequence of Params to be read from their log file
PARAMS = [var for var in locals().values() if isinstance(var, Param)]
