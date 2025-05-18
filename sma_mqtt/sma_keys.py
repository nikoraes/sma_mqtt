# SMA keys and Home Assistant MQTT discovery info
# You can add more keys/entities as needed

# Mapping for Condition tags
CONDITION_MAP = {
    35: "Fault",
    303: "Off",
    307: "Ok",
    455: "Warning",
}

SMA_KEYS = {
    # key: (friendly_name, unit, device_class, state_class, icon, value_template, transform)
    "6180_08214800": (
        "Condition",
        "",
        None,
        None,
        "mdi:solar-power",
        None,
        lambda v: (
            CONDITION_MAP.get(v[0]["tag"])
            if v and isinstance(v, list) and isinstance(v[0], dict) and "tag" in v[0]
            else str(v)
        ),
    ),
    "6400_00260100": (
        "Total Yield",
        "kWh",
        "energy",
        "total_increasing",
        "mdi:counter",
        None,
        lambda v: float(v) / 1000 if v is not None else None,
    ),
    "6400_00262200": (
        "Daily Yield",
        "kWh",
        "energy",
        "total",
        "mdi:counter",
        None,
        lambda v: float(v) / 1000 if v is not None else None,
    ),
    "6100_40263F00": ("Power", "W", "power", "measurement", "mdi:flash", None, None),
    "6100_00465700": (
        "Grid Frequency",
        "Hz",
        "frequency",
        "measurement",
        "mdi:sine-wave",
        None,
        lambda v: int(float(v) / 100) if v is not None else None,
    ),
    "6100_40465300": (
        "Grid Current L1",
        "A",
        "current",
        "measurement",
        "mdi:current-ac",
        None,
        lambda v: float(v) / 1000 if v is not None else None,
    ),
    "6100_00464800": (
        "Grid Voltage L1",
        "V",
        "voltage",
        "measurement",
        "mdi:flash",
        None,
        lambda v: float(v) / 100 if v is not None else None,
    ),
    # Add more keys/entities here as needed
}

# Home Assistant MQTT Discovery base topic
HA_DISCOVERY_PREFIX = "homeassistant"
# Device info for Home Assistant
DEVICE_INFO = {
    "identifiers": ["sma_inverter"],
    "manufacturer": "SMA",
    "model": "Solar Inverter",
    "name": "SMA Inverter",
}
