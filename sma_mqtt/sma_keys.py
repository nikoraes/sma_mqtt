# SMA keys and Home Assistant MQTT discovery info
# You can add more keys/entities as needed

SMA_KEYS = {
    # key: (friendly_name, unit, device_class, state_class, icon, value_template)
    "6180_08214800": ("Condition", "", None, None, "mdi:solar-power", None),
    "6400_00260100": (
        "Total Yield",
        "Wh",
        "energy",
        "total_increasing",
        "mdi:counter",
        None,
    ),
    "6400_00262200": (
        "Daily Yield",
        "Wh",
        "energy",
        "total_increasing",
        "mdi:counter",
        None,
    ),
    "6100_40263F00": ("Power", "W", "power", "measurement", "mdi:flash", None),
    "6100_00465700": (
        "Grid Frequency",
        "Hz",
        "frequency",
        "measurement",
        "mdi:sine-wave",
        None,
    ),
    "6100_40465300": (
        "Grid Current L1",
        "A",
        "current",
        "measurement",
        "mdi:current-ac",
        None,
    ),
    "6100_00464800": (
        "Grid Voltage L1",
        "V",
        "voltage",
        "measurement",
        "mdi:flash",
        None,
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
