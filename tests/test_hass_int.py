# File: tests/test_hass_int.py

import pytest
from mtec2mqtt.hass_int import HassIntegration
from mtec2mqtt.mqtt_client import MqttClient


@pytest.fixture
def mock_hass_integration():
    hass_base_topic = "homeassistant"
    register_map = {
        "some_device": {
            "type": "sensor",
            "unique_id": "unique_sensor_id",
            "name": "Test Sensor",
        }
    }
    return HassIntegration(hass_base_topic, register_map)


def test_hass_integration_initialization(mock_hass_integration):
    assert mock_hass_integration.is_initialized is False


def test_hass_integration_initialize(mock_hass_integration, mocker):
    mqtt_client = mocker.Mock(spec=MqttClient)
    serial_no = "12345-67890"
    firmware_version = "1.0.0"
    equipment_info = "Test Equipment"

    mock_hass_integration.initialize(
        mqtt=mqtt_client,
        serial_no=serial_no,
        firmware_version=firmware_version,
        equipment_info=equipment_info,
    )
    assert mock_hass_integration.is_initialized is True


def test_hass_integration_send_discovery_info(mock_hass_integration, mocker):
    mock_hass_integration.send_discovery_info = mocker.Mock()
    mock_hass_integration.send_discovery_info()
    mock_hass_integration.send_discovery_info.assert_called_once()


def test_hass_integration_send_unregister_info(mock_hass_integration, mocker):
    mock_hass_integration.send_unregister_info = mocker.Mock()
    mock_hass_integration.send_unregister_info()
    mock_hass_integration.send_unregister_info.assert_called_once()


def test_hass_integration_build_automation_array(mock_hass_integration, mocker):
    mock_hass_integration._build_automation_array = mocker.Mock()
    mock_hass_integration._build_automation_array()
    mock_hass_integration._build_automation_array.assert_called_once()


def test_hass_integration_build_devices_array(mock_hass_integration, mocker):
    mock_hass_integration._build_devices_array = mocker.Mock()
    mock_hass_integration._build_devices_array()
    mock_hass_integration._build_devices_array.assert_called_once()


def test_hass_integration_append_sensor(mock_hass_integration, mocker):
    mock_hass_integration._append_sensor = mocker.Mock()
    item = {"type": "sensor", "name": "test_sensor"}
    mock_hass_integration._append_sensor(item)
    mock_hass_integration._append_sensor.assert_called_once_with(item)


def test_hass_integration_append_binary_sensor(mock_hass_integration, mocker):
    mock_hass_integration._append_binary_sensor = mocker.Mock()
    item = {"type": "binary_sensor", "name": "test_binary_sensor"}
    mock_hass_integration._append_binary_sensor(item)
    mock_hass_integration._append_binary_sensor.assert_called_once_with(item)


def test_hass_integration_append_number(mock_hass_integration, mocker):
    mock_hass_integration._append_number = mocker.Mock()
    item = {"type": "number", "name": "test_number"}
    mock_hass_integration._append_number(item)
    mock_hass_integration._append_number.assert_called_once_with(item)


def test_hass_integration_append_select(mock_hass_integration, mocker):
    mock_hass_integration._append_select = mocker.Mock()
    item = {"type": "select", "name": "test_select"}
    mock_hass_integration._append_select(item)
    mock_hass_integration._append_select.assert_called_once_with(item)


def test_hass_integration_append_switch(mock_hass_integration, mocker):
    mock_hass_integration._append_switch = mocker.Mock()
    item = {"type": "switch", "name": "test_switch"}
    mock_hass_integration._append_switch(item)
    mock_hass_integration._append_switch.assert_called_once_with(item)
