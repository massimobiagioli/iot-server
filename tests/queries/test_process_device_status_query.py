from unittest.mock import AsyncMock

import pytest

from src.queries.process_device_status_query import (
    ProcessDeviceStatusQuery,
    create_process_device_status_query_handler,
)


@pytest.mark.asyncio
async def test_process_device_status_query_connected(mock_prisma):
    """Test processing a device connected message"""
    # Arrange
    message = {
        "payload": {
            "device_type": "esp32",
            "device_id": "0c4f5500",
            "device_name": "tester",
        },
        "timestamp": 806226802,
        "event_type": "connected",
    }

    mock_device = {
        "id": "0c4f5500",
        "device_type": "esp32",
        "device_name": "tester",
        "is_connected": True,
        "last_seen": 806226802,
    }

    # Mock the upsert command handler behavior
    mock_prisma.device.find_unique = AsyncMock(return_value=None)
    mock_prisma.device.create = AsyncMock(return_value=mock_device)

    query = ProcessDeviceStatusQuery(message=message)

    # Act
    handler = create_process_device_status_query_handler(mock_prisma)
    result = await handler(query)

    # Assert
    assert result == mock_device
    mock_prisma.device.find_unique.assert_called_once_with(where={"id": "0c4f5500"})
    mock_prisma.device.create.assert_called_once_with(
        data={
            "id": "0c4f5500",
            "device_type": "esp32",
            "device_name": "tester",
            "is_connected": True,
            "last_seen": 806226802,
        }
    )


@pytest.mark.asyncio
async def test_process_device_status_query_disconnected(mock_prisma):
    """Test processing a device disconnected message"""
    # Arrange
    message = {
        "payload": {
            "device_type": "esp32",
            "device_id": "0c4f5500",
            "device_name": "tester",
        },
        "timestamp": 806226802,
        "event_type": "disconnected",
    }

    existing_device = {
        "id": "0c4f5500",
        "device_type": "esp32",
        "device_name": "tester",
        "is_connected": True,
        "last_seen": 806220000,
    }

    updated_device = {
        "id": "0c4f5500",
        "device_type": "esp32",
        "device_name": "tester",
        "is_connected": False,
        "last_seen": 806226802,
    }

    mock_prisma.device.find_unique = AsyncMock(return_value=existing_device)
    mock_prisma.device.update = AsyncMock(return_value=updated_device)

    query = ProcessDeviceStatusQuery(message=message)

    # Act
    handler = create_process_device_status_query_handler(mock_prisma)
    result = await handler(query)

    # Assert
    assert result == updated_device
    mock_prisma.device.find_unique.assert_called_once_with(where={"id": "0c4f5500"})
    mock_prisma.device.update.assert_called_once_with(
        where={"id": "0c4f5500"},
        data={
            "is_connected": False,
            "last_seen": 806226802,
            "device_type": "esp32",
            "device_name": "tester",
        },
    )


@pytest.mark.asyncio
async def test_process_device_status_query_invalid_message(mock_prisma):
    """Test processing an invalid message"""
    # Arrange
    invalid_message = {
        "payload": {
            "device_type": "esp32",
            # Missing device_id and device_name
        },
        "timestamp": 806226802,
        "event_type": "connected",
    }

    query = ProcessDeviceStatusQuery(message=invalid_message)

    # Act
    handler = create_process_device_status_query_handler(mock_prisma)
    result = await handler(query)

    # Assert
    assert result is None
    mock_prisma.device.find_unique.assert_not_called()
    mock_prisma.device.create.assert_not_called()
    mock_prisma.device.update.assert_not_called()


@pytest.mark.asyncio
async def test_process_device_status_query_exception_handling(mock_prisma):
    """Test exception handling in process device status query"""
    # Arrange
    message = {
        "payload": {
            "device_type": "esp32",
            "device_id": "0c4f5500",
            "device_name": "tester",
        },
        "timestamp": 806226802,
        "event_type": "connected",
    }

    # Mock an exception during database operation
    mock_prisma.device.find_unique = AsyncMock(side_effect=Exception("Database error"))

    query = ProcessDeviceStatusQuery(message=message)

    # Act
    handler = create_process_device_status_query_handler(mock_prisma)
    result = await handler(query)

    # Assert
    assert result is None
    mock_prisma.device.find_unique.assert_called_once_with(where={"id": "0c4f5500"})
