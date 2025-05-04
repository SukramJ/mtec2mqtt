# File: tests/test_modbus_client.py

from unittest.mock import MagicMock, patch

import pytest
from mtec2mqtt.const import RegisterGroup
from mtec2mqtt.modbus_client import MTECModbusClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu.register_read_message import ReadHoldingRegistersResponse


@pytest.fixture
def mock_modbus_client():
    config = {"host": "127.0.0.1", "port": 502}
    register_map = {"group1": {"register1": {"address": 0x01}}}
    register_groups = ["group1"]
    return MTECModbusClient(config, register_map, register_groups)


def test_initialization(mock_modbus_client):
    assert mock_modbus_client.register_groups == ["group1"]
    assert mock_modbus_client.register_map == {"group1": {"register1": {"address": 0x01}}}


def test_connect_successful(mock_modbus_client):
    with patch("pymodbus.client.ModbusTcpClient.connect", return_value=True):
        assert mock_modbus_client.connect() is True


def test_connect_failure(mock_modbus_client):
    with patch("pymodbus.client.ModbusTcpClient.connect", return_value=False):
        assert mock_modbus_client.connect() is False


def test_disconnect(mock_modbus_client):
    with patch("pymodbus.client.ModbusTcpClient.close") as mock_close:
        mock_modbus_client.disconnect()
        mock_close.assert_called_once()


def test_get_register_list(mock_modbus_client):
    group = RegisterGroup(name="group1")
    assert mock_modbus_client.get_register_list(group) == ["register1"]


def test_read_modbus_data(mock_modbus_client):
    mock_response = ReadHoldingRegistersResponse()
    with patch.object(mock_modbus_client, "_read_registers", return_value=mock_response):
        result = mock_modbus_client.read_modbus_data(["register1"])
        assert isinstance(result, dict)


def test_read_modbus_data_failure(mock_modbus_client):
    with patch.object(mock_modbus_client, "_read_registers", side_effect=ModbusException):
        result = mock_modbus_client.read_modbus_data(["register1"])
        assert result == {}


def test_write_register_by_name_success(mock_modbus_client):
    with patch.object(mock_modbus_client, "write_register", return_value=True):
        assert mock_modbus_client.write_register_by_name("register1", 10) is True


def test_write_register_by_name_failure(mock_modbus_client):
    with patch.object(mock_modbus_client, "write_register", return_value=False):
        assert mock_modbus_client.write_register_by_name("register1", 10) is False


def test_write_register_success(mock_modbus_client):
    with patch("pymodbus.client.ModbusTcpClient.write_register", return_value=0):
        assert mock_modbus_client.write_register("register1", 10) is True


def test_write_register_failure(mock_modbus_client):
    with patch("pymodbus.client.ModbusTcpClient.write_register", side_effect=ModbusException):
        assert mock_modbus_client.write_register("register1", 10) is False


def test_get_register_clusters(mock_modbus_client):
    with patch.object(mock_modbus_client, "_generate_register_clusters", return_value=[{"foo": "bar"}]):
        clusters = mock_modbus_client._get_register_clusters(["register1"])
        assert clusters == [{"foo": "bar"}]


def test_generate_register_clusters(mock_modbus_client):
    clusters = mock_modbus_client._generate_register_clusters(["register1"])
    assert isinstance(clusters, list)


def test_read_registers_success(mock_modbus_client):
    mock_response = ReadHoldingRegistersResponse()
    with patch.object(mock_modbus_client, "_read_registers", return_value=mock_response):
        response = mock_modbus_client._read_registers("register1", 1)
        assert response == mock_response


def test_read_registers_failure(mock_modbus_client):
    with patch.object(mock_modbus_client, "_read_registers", side_effect=ModbusException):
        response = mock_modbus_client._read_registers("register1", 1)
        assert response is None
