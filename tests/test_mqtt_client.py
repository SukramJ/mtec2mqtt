from unittest.mock import MagicMock, patch

import pytest
from mtec2mqtt.const import Config
from mtec2mqtt.mqtt_client import MqttClient


@pytest.fixture
def mock_config():
    return {
        Config.MQTT_LOGIN: "test_user",
        Config.MQTT_PASSWORD: "test_pass",
        Config.MQTT_SERVER: "localhost",
        Config.MQTT_PORT: 1883,
        Config.HASS_BASE_TOPIC: "home",
    }


@pytest.fixture
def mock_on_mqtt_message():
    return MagicMock()


@pytest.fixture
def mqtt_client(mock_config, mock_on_mqtt_message):
    return MqttClient(config=mock_config, on_mqtt_message=mock_on_mqtt_message)


def test_mqtt_client_initialization(mock_config, mock_on_mqtt_message):
    client = MqttClient(config=mock_config, on_mqtt_message=mock_on_mqtt_message)
    assert client is not None


def test_mqtt_client_stop(mqtt_client):
    with patch.object(mqtt_client, "_client", MagicMock()) as mock_client:
        mqtt_client.stop()
        mock_client.loop_stop.assert_called_once()


def test_mqtt_client_publish(mqtt_client):
    with patch.object(mqtt_client, "_client", MagicMock()) as mock_client:
        mqtt_client.publish("test/topic", "payload", retain=True)
        mock_client.publish.assert_called_once_with(
            topic="test/topic", payload="payload", retain=True
        )


def test_mqtt_client_subscribe_to_topic(mqtt_client):
    with patch.object(mqtt_client, "_client", MagicMock()) as mock_client:
        mqtt_client.subscribe_to_topic("test/topic")
        mock_client.subscribe_to_topic.assert_called_once_with(topic="test/topic")


def test_mqtt_client_unsubscribe_from_topic(mqtt_client):
    mqtt_client._subscribed_topics.add("test/topic")
    with patch.object(mqtt_client, "_client", MagicMock()) as mock_client:
        mqtt_client.unsubscribe_from_topic("test/topic")
        mock_client.unsubscribe_from_topic.assert_called_once_with(topic="test/topic")
        assert "test/topic" not in mqtt_client._subscribed_topics


def test_mqtt_client_on_mqtt_connect(mqtt_client):
    with patch("mtec2mqtt.mqtt_client._LOGGER.info") as mock_log:
        mqtt_client.on_mqtt_connect()
        mock_log.assert_called_once_with("Connected to MQTT broker")
