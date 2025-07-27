import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src import handle_device_status_message


@pytest.mark.asyncio
async def test_handle_device_status_message_valid_json():
    """Test that valid JSON messages are processed correctly"""
    # Arrange
    client = MagicMock()
    topic = "device_status"
    valid_message = {
        "payload": {
            "device_type": "esp32",
            "device_id": "test123",
            "device_name": "test_device",
        },
        "timestamp": 1234567890,
        "event_type": "connected",
    }
    payload = json.dumps(valid_message).encode()
    qos = 1
    properties = {}

    # Mock the query handler
    with patch("src.create_process_device_status_query_handler") as mock_create_handler:
        mock_handler = AsyncMock()
        mock_create_handler.return_value = mock_handler

        # Act
        await handle_device_status_message(client, topic, payload, qos, properties)

        # Assert
        mock_create_handler.assert_called_once()
        mock_handler.assert_called_once()


@pytest.mark.asyncio
async def test_handle_device_status_message_invalid_json():
    """Test that invalid JSON messages are rejected and logged"""
    # Arrange
    client = MagicMock()
    topic = "device_status"
    invalid_payload = b"{'this': 'is not valid json'}"  # Python dict format
    qos = 1
    properties = {}

    # Mock the query handler
    with patch("src.create_process_device_status_query_handler") as mock_create_handler:
        mock_handler = AsyncMock()
        mock_create_handler.return_value = mock_handler

        # Mock print to capture error messages
        with patch("builtins.print") as mock_print:
            # Act
            await handle_device_status_message(
                client, topic, invalid_payload, qos, properties
            )

            # Assert
            mock_create_handler.assert_not_called()
            mock_handler.assert_not_called()

            # Check that error was logged
            mock_print.assert_called()
            error_calls = [
                call
                for call in mock_print.call_args_list
                if "Invalid JSON" in str(call)
            ]
            assert len(error_calls) > 0


@pytest.mark.asyncio
async def test_handle_device_status_message_malformed_payload():
    """Test that completely malformed payloads are rejected"""
    # Arrange
    client = MagicMock()
    topic = "device_status"
    malformed_payload = b"this is not json at all!!!"
    qos = 1
    properties = {}

    # Mock the query handler
    with patch("src.create_process_device_status_query_handler") as mock_create_handler:
        mock_handler = AsyncMock()
        mock_create_handler.return_value = mock_handler

        # Mock print to capture error messages
        with patch("builtins.print") as mock_print:
            # Act
            await handle_device_status_message(
                client, topic, malformed_payload, qos, properties
            )

            # Assert
            mock_create_handler.assert_not_called()
            mock_handler.assert_not_called()

            # Check that error was logged
            mock_print.assert_called()
            error_calls = [
                call
                for call in mock_print.call_args_list
                if "Invalid JSON" in str(call)
            ]
            assert len(error_calls) > 0


@pytest.mark.asyncio
async def test_handle_device_status_message_processing_error():
    """Test that processing errors are handled gracefully"""
    # Arrange
    client = MagicMock()
    topic = "device_status"
    valid_message = {"test": "message"}
    payload = json.dumps(valid_message).encode()
    qos = 1
    properties = {}

    # Mock the query handler to raise an exception
    with patch("src.create_process_device_status_query_handler") as mock_create_handler:
        mock_handler = AsyncMock()
        mock_handler.side_effect = Exception("Processing error")
        mock_create_handler.return_value = mock_handler

        # Mock print to capture error messages
        with patch("builtins.print") as mock_print:
            # Act
            await handle_device_status_message(client, topic, payload, qos, properties)

            # Assert
            mock_create_handler.assert_called_once()
            mock_handler.assert_called_once()

            # Check that error was logged
            mock_print.assert_called()
            error_calls = [
                call
                for call in mock_print.call_args_list
                if "Error handling device status message" in str(call)
            ]
            assert len(error_calls) > 0
