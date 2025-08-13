"""
Home Assistant MQTT discovery integration.

Constructs and publishes MQTT discovery payloads for sensors, binary sensors,
number/select/switch entities, and optional custom automations. It uses the
register map to determine which entities should be exposed and subscribes to
command topics for controllable entities.

(c) 2024 by Christian Rödel
(c) 2024 by SukramJ
"""

from __future__ import annotations

import json
import logging
from typing import Any, Final

from mtec2mqtt import mqtt_client
from mtec2mqtt.const import HA, MTEC_PREFIX, MTEC_TOPIC_ROOT, HAPlatform, Register

_LOGGER: Final = logging.getLogger(__name__)


class HassIntegration:
    """HA integration."""

    # Custom automations
    buttons: list[str] = [
        # name                        unique_id                   payload_press
        #    [ "Set general mode",         "MTEC_load_battery_btn",    "load_battery_from_grid" ],
    ]

    def __init__(self, hass_base_topic: str, register_map: dict[str, dict[str, Any]]) -> None:
        """Init hass integration."""
        self._hass_base_topic: Final = hass_base_topic
        self._register_map: Final = register_map
        self._mqtt: mqtt_client.MqttClient = None  # type: ignore[assignment]
        self._serial_no: str | None = None
        self._is_initialized = False
        self._devices_array: Final[list[tuple[str, Any]]] = []
        self._device_info: dict[str, Any] = {}

    @property
    def is_initialized(self) -> bool:
        """Return True if hass integration initialized."""
        return self._is_initialized

    def initialize(
        self,
        mqtt: mqtt_client.MqttClient,
        serial_no: str,
        firmware_version: str,
        equipment_info: str,
    ) -> None:
        """Initialize."""
        self._mqtt = mqtt
        self._serial_no = serial_no
        self._device_info = {
            HA.IDENTIFIERS: [serial_no],
            HA.MANUFACTURER: "M-TEC",
            HA.MODEL: "Energy-Butler",
            HA.MODEL_ID: equipment_info,
            HA.NAME: "MTEC EnergyButler",
            HA.SERIAL_NUMBER: serial_no,
            HA.SW_VERSION: firmware_version,
        }
        self._devices_array.clear()
        self._build_devices_array()
        self._build_automation_array()
        self.send_discovery_info()
        self._is_initialized = True

    def send_discovery_info(self) -> None:
        """Send discovery info."""
        _LOGGER.info("Sending home assistant discovery info")
        for device in self._devices_array:
            topic = device[0]
            payload = device[1]
            self._mqtt.publish(topic=topic, payload=payload, retain=True)
            if HA.COMMAND_TOPIC in payload:
                data = json.loads(payload)
                if command_topic := data.get(HA.COMMAND_TOPIC):
                    self._mqtt.subscribe_to_topic(topic=command_topic)

    def send_unregister_info(self) -> None:
        """Send unregister info."""
        _LOGGER.info("Sending info to unregister from home assistant")
        for device in self._devices_array:
            self._mqtt.publish(topic=device[0], payload="")

    def _build_automation_array(self) -> None:
        # Buttons
        for item in self.buttons:
            data_item = {
                HA.COMMAND_TOPIC: f"{MTEC_TOPIC_ROOT}/{self._serial_no}/automations/command",
                HA.DEVICE: self._device_info,
                HA.NAME: item[0],
                HA.PAYLOAD_PRESS: item[2],
                HA.UNIQUE_ID: item[1],
            }
            topic = f"{self._hass_base_topic}/button/{item[1]}/config"
            self._devices_array.append((topic, json.dumps(data_item)))

    def _build_devices_array(self) -> None:
        """Build discovery data for devices."""
        for item in self._register_map.values():
            # Do registration if there is a "hass_" config entry
            do_hass_registration = False
            for key in item:
                if "hass_" in key:
                    do_hass_registration = True
                    break

            if item[Register.GROUP] and do_hass_registration:
                component_type = item.get(Register.COMPONENT_TYPE, HAPlatform.SENSOR)
                if component_type == HAPlatform.SENSOR:
                    self._append_sensor(item)
                elif component_type == HAPlatform.BINARY_SENSOR:
                    self._append_binary_sensor(item)
                elif component_type == HAPlatform.NUMBER:
                    self._append_number(item)
                    self._append_sensor(item)
                elif component_type == HAPlatform.SELECT:
                    self._append_select(item)
                    self._append_sensor(item)
                elif component_type == HAPlatform.SWITCH:
                    self._append_switch(item)
                    self._append_binary_sensor(item)

    def _append_sensor(self, item: dict[str, Any]) -> None:
        data_item = {
            HA.DEVICE: self._device_info,
            HA.ENABLED_BY_DEFAULT: True,
            HA.NAME: item[Register.NAME],
            HA.STATE_TOPIC: f"{MTEC_TOPIC_ROOT}/{self._serial_no}/{item[Register.GROUP]}/{item[Register.MQTT]}/state",
            HA.UNIQUE_ID: f"{MTEC_PREFIX}{item[Register.MQTT]}",
            HA.UNIT_OF_MEASUREMENT: item[Register.UNIT],
        }
        if hass_device_class := item.get(Register.DEVICE_CLASS):
            data_item[HA.DEVICE_CLASS] = hass_device_class
        if hass_value_template := item.get(Register.VALUE_TEMPLATE):
            data_item[HA.VALUE_TEMPLATE] = hass_value_template
        if hass_state_class := item.get(Register.STATE_CLASS):
            data_item[HA.STATE_CLASS] = hass_state_class

        topic = f"{self._hass_base_topic}/{HAPlatform.SENSOR}/{MTEC_PREFIX}{item[Register.MQTT]}/config"
        self._devices_array.append((topic, json.dumps(data_item)))

    def _append_binary_sensor(self, item: dict[str, Any]) -> None:
        data_item = {
            HA.DEVICE: self._device_info,
            HA.ENABLED_BY_DEFAULT: True,
            HA.NAME: item[Register.NAME],
            HA.STATE_TOPIC: f"{MTEC_TOPIC_ROOT}/{self._serial_no}/{item[Register.GROUP]}/{item[Register.MQTT]}/state",
            HA.UNIQUE_ID: f"{MTEC_PREFIX}{item[Register.MQTT]}",
        }

        if hass_device_class := item.get(Register.DEVICE_CLASS):
            data_item[HA.DEVICE_CLASS] = hass_device_class
        if hass_payload_on := item.get(Register.PAYLOAD_ON):
            data_item[HA.PAYLOAD_ON] = hass_payload_on
        if hass_payload_off := item.get(Register.PAYLOAD_OFF):
            data_item[HA.PAYLOAD_OFF] = hass_payload_off

        topic = f"{self._hass_base_topic}/{HAPlatform.BINARY_SENSOR}/{MTEC_PREFIX}{item[Register.MQTT]}/config"
        self._devices_array.append((topic, json.dumps(data_item)))

    def _append_number(self, item: dict[str, Any]) -> None:
        mtec_topic = (
            f"{MTEC_TOPIC_ROOT}/{self._serial_no}/{item[Register.GROUP]}/{item[Register.MQTT]}"
        )
        data_item = {
            HA.COMMAND_TOPIC: f"{mtec_topic}/set",
            HA.DEVICE: self._device_info,
            HA.ENABLED_BY_DEFAULT: False,
            HA.MODE: "box",
            HA.NAME: item[Register.NAME],
            HA.STATE_TOPIC: f"{mtec_topic}/state",
            HA.UNIQUE_ID: f"{MTEC_PREFIX}{item[Register.MQTT]}",
            HA.UNIT_OF_MEASUREMENT: item[Register.UNIT],
        }

        if hass_device_class := item.get(Register.DEVICE_CLASS):
            data_item[HA.DEVICE_CLASS] = hass_device_class

        topic = f"{self._hass_base_topic}/{HAPlatform.NUMBER}/{MTEC_PREFIX}{item[Register.MQTT]}/config"
        self._devices_array.append((topic, json.dumps(data_item)))

    def _append_select(self, item: dict[str, Any]) -> None:
        options = item[Register.VALUE_ITEMS]
        mtec_topic = (
            f"{MTEC_TOPIC_ROOT}/{self._serial_no}/{item[Register.GROUP]}/{item[Register.MQTT]}"
        )
        data_item = {
            HA.COMMAND_TOPIC: f"{mtec_topic}/set",
            HA.DEVICE: self._device_info,
            HA.ENABLED_BY_DEFAULT: False,
            HA.NAME: item[Register.NAME],
            HA.OPTIONS: list(options.values()),
            HA.STATE_TOPIC: f"{mtec_topic}/state",
            HA.UNIQUE_ID: f"{MTEC_PREFIX}{item[Register.MQTT]}",
        }

        topic = f"{self._hass_base_topic}/{HAPlatform.SELECT}/{MTEC_PREFIX}{item[Register.MQTT]}/config"
        self._devices_array.append((topic, json.dumps(data_item)))

    def _append_switch(self, item: dict[str, Any]) -> None:
        mtec_topic = (
            f"{MTEC_TOPIC_ROOT}/{self._serial_no}/{item[Register.GROUP]}/{item[Register.MQTT]}"
        )
        data_item = {
            HA.COMMAND_TOPIC: f"{mtec_topic}/set",
            HA.DEVICE: self._device_info,
            HA.ENABLED_BY_DEFAULT: False,
            HA.NAME: item[Register.NAME],
            HA.STATE_TOPIC: f"{mtec_topic}/state",
            HA.UNIQUE_ID: f"{MTEC_PREFIX}{item[Register.MQTT]}",
        }

        if hass_device_class := item.get(Register.DEVICE_CLASS):
            data_item[HA.DEVICE_CLASS] = hass_device_class
        if hass_payload_on := item.get(Register.PAYLOAD_ON):
            data_item[HA.PAYLOAD_ON] = hass_payload_on
        if hass_payload_off := item.get(Register.PAYLOAD_OFF):
            data_item[HA.PAYLOAD_OFF] = hass_payload_off

        topic = f"{self._hass_base_topic}/{HAPlatform.SWITCH}/{MTEC_PREFIX}{item[Register.MQTT]}/config"
        self._devices_array.append((topic, json.dumps(data_item)))
