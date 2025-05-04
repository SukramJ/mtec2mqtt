from unittest.mock import Mock, patch

import pytest
from mtec2mqtt.const import RegisterGroup
from mtec2mqtt.mtec_coordinator import MtecCoordinator


def test_mtec_coordinator_initialization():
    coordinator = MtecCoordinator()
    assert isinstance(coordinator, MtecCoordinator)


def test_mtec_coordinator_run():
    coordinator = MtecCoordinator()
    with patch("mtec2mqtt.mtec_coordinator.signal.signal") as mock_signal, \
            patch("mtec2mqtt.mtec_coordinator.time.sleep", side_effect=KeyboardInterrupt):
        coordinator.run()
        mock_signal.assert_called()


def test_mtec_coordinator_stop():
    coordinator = MtecCoordinator()
    coordinator.stop()
    # Placeholder for further assertions related to stop functionality


def test_mtec_coordinator_on_mqtt_message():
    coordinator = MtecCoordinator()
    client = Mock()
    userdata = Mock()
    message = Mock()
    message.payload = b'test'

    with patch("mtec2mqtt.mtec_coordinator.MtecCoordinator._on_mqtt_message") as mock_handler:
        coordinator._on_mqtt_message(client, userdata, message)
        mock_handler.assert_called_with(client, userdata, message)


def test_mtec_coordinator_read_mtec_data():
    coordinator = MtecCoordinator()
    group = Mock(spec=RegisterGroup)
    with patch("mtec2mqtt.mtec_coordinator.MtecCoordinator.read_mtec_data",
               return_value={"data": "value"}) as mock_read:
        data = coordinator.read_mtec_data(group)
        mock_read.assert_called_with(group)
        assert data == {"data": "value"}


def test_mtec_coordinator_write_to_mqtt():
    coordinator = MtecCoordinator()
    pvdata = {"test_key": "test_value"}
    topic_base = "test/topic"
    group = Mock(spec=RegisterGroup)

    with patch("mtec2mqtt.mtec_coordinator.MtecCoordinator.write_to_mqtt") as mock_write:
        coordinator.write_to_mqtt(pvdata, topic_base, group)
        mock_write.assert_called_with(pvdata, topic_base, group)
