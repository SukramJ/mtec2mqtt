"""
MQTT client base implementation.

(c) 2024 by Christian Rödel
(c) 2024 by SukramJ
"""

from __future__ import annotations

from collections.abc import Callable
from copy import copy
import logging
from typing import Any, Final

from paho.mqtt import client as mqtt

from mtec2mqtt import hass_int
from mtec2mqtt.const import CLIENT_ID, Config
from mtec2mqtt.exceptions import MtecException

DEFAULT_RETAIN: bool = False
_LOGGER: Final = logging.getLogger(__name__)


class MqttClient:
    """Client for mqtt."""

    def __init__(
        self,
        config: dict[str, Any],
        on_mqtt_message: Callable,
        hass: hass_int.HassIntegration | None = None,
    ) -> None:
        """Init the mqtt client."""
        self._on_mqtt_message = on_mqtt_message
        self._hass = hass
        self._username: Final[str] = config[Config.MQTT_LOGIN]
        self._password: Final[str] = config[Config.MQTT_PASSWORD]
        self._auth: Final[dict[str, str]] = {
            "username": self._username,
            "password": self._password,
        }
        self._hostname: Final[str] = config[Config.MQTT_SERVER]
        self._port: Final[int] = config[Config.MQTT_PORT]
        self._hass_status_topic: Final[str] = f"{config[Config.HASS_BASE_TOPIC]}/status"
        self._client = self._initialize_client()
        self._subscribed_topics: set[str] = set()

    def on_mqtt_connect(self, *args: Any) -> None:
        """Handle mqtt connect."""
        _LOGGER.info("Connected to MQTT broker")

    def _initialize_client(self) -> mqtt.Client:
        """Initialize and start the MQTT client."""
        try:
            client = mqtt.Client(client_id=CLIENT_ID)
            client.username_pw_set(username=self._username, password=self._password)
            client.connect(host=self._hostname, port=self._port)

            if self._hass:
                client.subscribe_to_topic(topic=self._hass_status_topic)
            client.on_connect = self.on_mqtt_connect
            client.on_message = self._on_mqtt_message
            client.loop_start()
            _LOGGER.info("MQTT server started")
        except Exception as ex:
            msg = "Couldn't start MQTT: {str(e)}"
            _LOGGER.warning(msg)
            raise MtecException(msg) from ex
        else:
            return client

    def stop(self) -> None:
        """Stop the MQTT client."""
        try:
            for topic in copy(self._subscribed_topics):
                self.unsubscribe_from_topic(topic=topic)
            self._client.loop_stop()
            _LOGGER.info("MQTT server stopped")
        except Exception as e:
            _LOGGER.warning("Couldn't stop MQTT: %s", str(e))

    def publish(self, topic: str, payload: str, retain: bool = DEFAULT_RETAIN) -> None:
        """Publish mqtt message."""
        _LOGGER.debug("- %s: %s", topic, str(payload))
        try:
            self._client.publish(topic=topic, payload=payload, retain=retain)
        except Exception as e:
            _LOGGER.error("Couldn't send MQTT command: %s", str(e))

    def subscribe_to_topic(self, topic: str) -> None:
        """Subscribe on topic."""
        _LOGGER.debug("subscribe on %s", topic)
        try:
            if topic in self._subscribed_topics:
                return
            self._client.subscribe_to_topic(topic=topic)
            self._subscribed_topics.add(topic)
        except Exception as ex:
            _LOGGER.error("Couldn't subscribe on MQTT topic: %s: %s", topic, ex)

    def unsubscribe_from_topic(self, topic: str) -> None:
        """Unsubscribe from topic."""
        _LOGGER.debug("unsubscribe from %s", topic)
        try:
            if topic not in self._subscribed_topics:
                return
            self._client.unsubscribe_from_topic(topic=topic)
            self._subscribed_topics.remove(topic)
        except Exception as ex:
            _LOGGER.error("Couldn't unsubscribe from MQTT topic: %s: %s", topic, ex)
