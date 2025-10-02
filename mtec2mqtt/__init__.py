"""
Top-level package for mtec2mqtt.

Provides MQTT publication of values read from an M-TEC Energybutler via
Modbus, optional Home Assistant discovery integration, and small utilities.
"""

from __future__ import annotations

__all__ = ["config", "mqtt_client", "hass_int", "modbus_client"]
__version__ = "2.0.5"
