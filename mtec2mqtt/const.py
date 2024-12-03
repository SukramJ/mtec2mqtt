"""mtec2mqtt constants."""

from __future__ import annotations

from enum import StrEnum
from typing import Final

CLIENT_ID: Final = "M-TEC-MQTT"
CONFIG_FILE: Final = "config.yaml"
CONFIG_PATH: Final = "mtec2mqtt"
CONFIG_ROOT: Final = ".config"
CONFIG_TEMPLATE: Final = "config-template.yaml"
DEFAULT_FRAMER: Final = "rtu"
UTF8: Final = "utf-8"


class Config(StrEnum):
    """enum with config qualifiers."""

    DEBUG = "DEBUG"
    HASS_BASE_TOPIC = "HASS_BASE_TOPIC"
    HASS_BIRTH_GRACETIME = "HASS_BIRTH_GRACETIME"
    HASS_ENABLE = "HASS_ENABLE"
    MODBUS_FRAMER = "MODBUS_FRAMER"
    MODBUS_IP = "MODBUS_IP"
    MODBUS_PORT = "MODBUS_PORT"
    MODBUS_RETRIES = "MODBUS_RETRIES"
    MODBUS_SLAVE = "MODBUS_SLAVE"
    MODBUS_TIMEOUT = "MODBUS_TIMEOUT"
    MQTT_FLOAT_FORMAT = "MQTT_FLOAT_FORMAT"
    MQTT_LOGIN = "MQTT_LOGIN"
    MQTT_PASSWORD = "MQTT_PASSWORD"
    MQTT_PORT = "MQTT_PORT"
    MQTT_SERVER = "MQTT_SERVER"
    MQTT_TOPIC = "MQTT_TOPIC"
    REFRESH_CONFIG = "REFRESH_CONFIG"
    REFRESH_DAY = "REFRESH_DAY"
    REFRESH_NOW = "REFRESH_NOW"
    REFRESH_TOTAL = "REFRESH_TOTAL"


class HA(StrEnum):
    """Enum with HA qualifiers."""

    COMMAND_TOPIC = "command_topic"
    DEVICE = "device"
    DEVICE_CLASS = "device_class"
    IDENTIFIERS = "identifiers"
    MANUFACTURER = "manufacturer"
    MODEL = "model"
    NAME = "name"
    PAYLOAD_OFF = "payload_off"
    PAYLOAD_ON = "payload_on"
    PAYLOAD_PRESS = "payload_press"
    SERIAL_NUMBER = "serial_number"
    STATE_CLASS = "state_class"
    STATE_TOPIC = "state_topic"
    UNIQUE_ID = "unique_id"
    SW_VERSION = "sw_version"
    UNIT_OF_MEASUREMENT = "unit_of_measurement"
    VALUE_TEMPLATE = "value_template"
    VIA_DEVICE = "via_device"


class Register(StrEnum):
    """Enum with Register qualifiers."""

    DEVICE_CLASS = "hass_device_class"
    FIRMWARE_VERSION = "firmware_version"
    GROUP = "group"
    LENGTH = "length"
    MQTT = "mqtt"
    NAME = "name"
    PAYLOAD_OFF = "hass_payload_off"
    PAYLOAD_ON = "hass_payload_on"
    SCALE = "scale"
    SERIAL_NO = "serial_no"
    STATE_CLASS = "hass_state_class"
    TYPE = "type"
    UNIT = "unit"
    VALUE = "value"
    VALUE_TEMPLATE = "hass_value_template"
    WRITABLE = "writable"


class RegisterGroup(StrEnum):
    """Enum with Register group qualifiers."""

    BASE = "now-base"
    GRID = "now-grid"
    INVERTER = "now-inverter"
    BACKUP = "now-backup"
    BATTERY = "now-battery"
    PV = "now-pv"
    CONFIG = "config"
    DAY = "day"
    TOTAL = "total"


SECONDARY_REGISTER_GROUPS: Final = {
    0: RegisterGroup.GRID,
    1: RegisterGroup.INVERTER,
    2: RegisterGroup.BACKUP,
    3: RegisterGroup.BATTERY,
    4: RegisterGroup.PV,
}

BMS_ALARM_CODES: Final = {
    2: "Cells High Voltage Warning",
    4: "Battery Module Discharge Low Voltage Warning",
    8: "Battery Module Charge Over Voltage Warning",
    16: "Charge Low Temperature Warning",
    32: "Charge Over Temperature Warning",
    64: "Discharge Low Temperature Warning",
    128: "Discharge Over Temperature Warning",
    256: "Battery Module Charge Over Current Warning",
    512: "Battery Module Discharge Over Current Warning",
    1024: "Battery Module Low Voltage Warning",
    2048: "Battery Module Over Voltage Warning",
    4096: "Power Terminal Over Temperature Warning",
    8192: "Ambient Low Temperature Warning",
    16384: "Ambient Over Temperature Warning",
}

BMS_FAULT_CODES: Final = {
    1: "Internal COM Fault",
    2: "Voltage Sensor Fault",
    4: "Temperature Sensor Fault",
    8: "Relay Fault",
    16: "Cells Damage Fault",
}

BMS_PROTECTION_CODES: Final = {
    2: "Cells High Voltage Protection",
    4: "Battery Module Discharge Low Voltage Protection",
    8: "Battery Module Charge Over Voltage Protection",
    16: "Charge Low Temperature Protection",
    32: "Charge Over Temperature Protection",
    64: "Discharge Low Temperature Protection",
    128: "Discharge Over Temperature Protection",
    256: "Battery Module Charge Over Current Protection",
    512: "Battery Module Discharge Over Current Protection",
    1024: "Battery Module Low Voltage Protection",
    2048: "Battery Module Over Voltage Protection",
    4096: "Power Terminal Over Temperature Protection",
    8192: "Ambient Low Temperature Protection",
    16384: "Ambient High Temperature Protection",
    32768: "Leakage Current Protection",
}

FAULT_FLAGS_1: Final = {
    1: "Mains Lost",
    2: "Grid Voltage Fault",
    4: "Grid Frequency Fault",
    8: "DCI Fault",
    16: "ISO Over Limitation",
    32: "GFCI Fault",
    64: "PV Over Voltage",
    128: "Bus Voltage Fault",
}

FAULT_FLAGS_2: Final = {
    2: "SPI Fault",
    4: "E2 Fault",
    8: "GFCI Device Fault",
    16: "AC Transducer Fault",
    32: "Relay Check Fail",
    64: "Iternal Fan Fault",
    128: "External Fan Fault",
}

ENUM_REGISTER_CODES: Final = {
    "10112": FAULT_FLAGS_1,
    "10114": FAULT_FLAGS_2,
    "53509": BMS_FAULT_CODES,
    "53511": BMS_PROTECTION_CODES,
    "53513": BMS_ALARM_CODES,
}
