"""
MQTT client wrapper for publishing and subscribing to an MQTT broker.

This module encapsulates connection management (connect, disconnect, loop),
publication (with optional retain), and topic subscription bookkeeping. It is
used by the coordinator and, when enabled, integrates with Home Assistant by
subscribing to its status topic so discovery can be coordinated.

(c) 2024 by Christian Rödel
(c) 2024 by SukramJ
"""

from __future__ import annotations

from collections.abc import Callable
import contextlib
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
        on_mqtt_message: Callable[[mqtt.Client, Any, mqtt.MQTTMessage], None],
        hass: hass_int.HassIntegration | None = None,
    ) -> None:
        """Init the mqtt client."""
        self._on_mqtt_message = on_mqtt_message
        self._hass = hass
        self._username: Final[str] = config[Config.MQTT_LOGIN]
        self._password: Final[str] = config[Config.MQTT_PASSWORD]
        self._hostname: Final[str] = config[Config.MQTT_SERVER]
        self._port: Final[int] = config[Config.MQTT_PORT]
        self._hass_status_topic: Final[str] = f"{config[Config.HASS_BASE_TOPIC]}/status"
        self._client = self._initialize_client()
        self._subscribed_topics: set[str] = set()

    def _on_mqtt_connect(
        self, mqttclient: mqtt.Client, userdata: Any, flags: Any, rc: Any
    ) -> None:
        """Handle mqtt connect."""
        if rc == 0:
            _LOGGER.info("Connected to MQTT broker")
        else:
            _LOGGER.error("Error while connecting to MQTT broker: rc=%s", rc)

    def _on_mqtt_disconnect(self, mqttclient: mqtt.Client, userdata: Any, rc: Any) -> None:
        _LOGGER.warning("MQTT broker disconnected: rc=%s", rc)

    def _on_mqtt_subscribe(
        self, mqttclient: mqtt.Client, userdata: Any, mid: Any, granted_qos: Any
    ) -> None:
        _LOGGER.info("MQTT broker subscribed to mid %s", mid)

    def _initialize_client(self) -> mqtt.Client:
        """Initialize and start the MQTT client (non-blocking, with auto-reconnect)."""
        try:
            client = mqtt.Client(client_id=CLIENT_ID)
            client.username_pw_set(username=self._username, password=self._password)
            # Set handlers before connecting to avoid missing early events
            client.on_connect = self._on_mqtt_connect
            client.on_message = self._on_mqtt_message
            client.on_subscribe = self._on_mqtt_subscribe
            client.on_disconnect = self._on_mqtt_disconnect

            # Set a Last Will and Testament to signal unexpected offline state
            client.will_set(
                topic=f"{self._hass_status_topic}/lwt",
                payload="offline",
                retain=True,
            )

            # Configure exponential reconnect backoff to reduce tight retry loops
            client.reconnect_delay_set(min_delay=1, max_delay=120)

            # Use async connect to avoid blocking and enable auto-reconnect in loop
            client.connect_async(host=self._hostname, port=self._port)

            if self._hass:
                client.subscribe(topic=self._hass_status_topic)
            client.loop_start()
            _LOGGER.info("MQTT server started")
        except Exception as ex:
            msg = f"Couldn't start MQTT: {ex}"
            _LOGGER.warning(msg)
            raise MtecException(msg) from ex
        else:
            return client

    def stop(self) -> None:
        """Stop the MQTT client."""
        try:
            for topic in list(self._subscribed_topics):
                self.unsubscribe_from_topic(topic=topic)
            # Perform a graceful disconnect before stopping the loop
            with contextlib.suppress(Exception):
                self._client.disconnect()

            self._client.loop_stop()
            _LOGGER.info("MQTT server stopped")
        except Exception as ex:
            _LOGGER.warning("Couldn't stop MQTT: %s", ex)

    def publish(self, topic: str, payload: str, retain: bool = DEFAULT_RETAIN) -> None:
        """Publish mqtt message."""
        _LOGGER.debug("- %s: %s", topic, str(payload))
        try:
            self._client.publish(topic=topic, payload=payload, retain=retain)
        except Exception as ex:
            _LOGGER.error("Couldn't send MQTT command: %s", ex)

    def subscribe_to_topic(self, topic: str) -> None:
        """Subscribe on topic."""
        _LOGGER.debug("subscribe on %s", topic)
        try:
            if topic in self._subscribed_topics:
                return
            self._client.subscribe(topic=topic)
            self._subscribed_topics.add(topic)
        except Exception as ex:
            _LOGGER.error("Couldn't subscribe on MQTT topic: %s: %s", topic, ex)

    def unsubscribe_from_topic(self, topic: str) -> None:
        """Unsubscribe from topic."""
        _LOGGER.debug("unsubscribe from %s", topic)
        try:
            if topic not in self._subscribed_topics:
                return
            self._client.unsubscribe(topic=topic)
            self._subscribed_topics.remove(topic)
        except Exception as ex:
            _LOGGER.error("Couldn't unsubscribe from MQTT topic: %s: %s", topic, ex)
