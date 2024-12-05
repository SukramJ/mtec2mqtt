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
MTEC_TOPIC_ROOT: Final = "MTEC"
MTEC_PREFIX: Final = "MTEC_"
UTF8: Final = "utf-8"
ENV_XDG_CONFIG_HOME: Final = "XDG_CONFIG_HOME"
ENV_APPDATA: Final = "APPDATA"
FILE_REGISTERS: Final = "registers.yaml"


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
    REFRESH_STATIC = "REFRESH_STATIC"
    REFRESH_TOTAL = "REFRESH_TOTAL"


REFRESH_DEFAULTS: Final = {
    Config.REFRESH_CONFIG: 30,
    Config.REFRESH_DAY: 300,
    Config.REFRESH_NOW: 10,
    Config.REFRESH_STATIC: 3600,
    Config.REFRESH_TOTAL: 300,
}


class HA(StrEnum):
    """Enum with HA qualifiers."""

    COMMAND_TOPIC = "command_topic"
    DEVICE = "device"
    DEVICE_CLASS = "device_class"
    ENABLED_BY_DEFAULT = "enabled_by_default"
    IDENTIFIERS = "identifiers"
    MANUFACTURER = "manufacturer"
    MODE = "mode"
    MODEL = "model"
    NAME = "name"
    OPTIONS = "options"
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


class HAPlatform(StrEnum):
    """Enum with HA platform."""

    BINARY_SENSOR = "binary_sensor"
    NUMBER = "number"
    SELECT = "select"
    SENSOR = "sensor"
    SWITCH = "switch"


class Register(StrEnum):
    """Enum with Register qualifiers."""

    DEVICE_CLASS = "hass_device_class"
    FIRMWARE_VERSION = "firmware_version"
    GROUP = "group"
    COMPONENT_TYPE = "hass_component_type"
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
    VALUE_ITEMS = "hass_value_items"
    VALUE_TEMPLATE = "hass_value_template"
    WRITABLE = "writable"


class RegisterGroup(StrEnum):
    """Enum with Register group qualifiers."""

    BACKUP = "now-backup"
    BASE = "now-base"
    BATTERY = "now-battery"
    CONFIG = "config"
    DAY = "day"
    GRID = "now-grid"
    INVERTER = "now-inverter"
    PV = "now-pv"
    TOTAL = "total"
    STATIC = "static"


SECONDARY_REGISTER_GROUPS: Final = {
    0: RegisterGroup.GRID,
    1: RegisterGroup.INVERTER,
    2: RegisterGroup.BACKUP,
    3: RegisterGroup.BATTERY,
    4: RegisterGroup.PV,
}

MANDATORY_PARAMETERS: Final = [Register.NAME]

OPTIONAL_PARAMETERS: Final = {
    Register.LENGTH: None,
    Register.TYPE: None,
    Register.UNIT: "",
    Register.SCALE: 1,
    Register.WRITABLE: False,
    Register.MQTT: None,
    Register.GROUP: None,
}
