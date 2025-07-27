import pytest
from unittest.mock import AsyncMock

from src.commands.upsert_device_command import (
    UpsertDeviceCommand,
    create_upsert_device_command_handler,
)


@pytest.mark.asyncio
async def test_upsert_device_command_create_new_device(mock_prisma):
    """Test creating a new device when it doesn't exist"""
    # Arrange
    mock_prisma.device.find_unique = AsyncMock(return_value=None)
    mock_device = {
        "id": "test123",
        "device_type": "esp32",
        "device_name": "test_device",
        "is_connected": True,
        "last_seen": 123456789,
    }
    mock_prisma.device.create = AsyncMock(return_value=mock_device)

    command = UpsertDeviceCommand(
        device_id="test123",
        device_type="esp32",
        device_name="test_device",
        is_connected=True,
        last_seen=123456789,
    )

    # Act
    handler = create_upsert_device_command_handler(mock_prisma)
    result = await handler(command)

    # Assert
    mock_prisma.device.find_unique.assert_called_once_with(where={"id": "test123"})
    mock_prisma.device.create.assert_called_once_with(
        data={
            "id": "test123",
            "device_type": "esp32",
            "device_name": "test_device",
            "is_connected": True,
            "last_seen": 123456789,
        }
    )
    assert result == mock_device


@pytest.mark.asyncio
async def test_upsert_device_command_update_existing_device(mock_prisma):
    """Test updating an existing device"""
    # Arrange
    existing_device = {
        "id": "test123",
        "device_type": "esp8266",
        "device_name": "old_name",
        "is_connected": False,
        "last_seen": 111111111,
    }
    updated_device = {
        "id": "test123",
        "device_type": "esp32",
        "device_name": "new_name",
        "is_connected": True,
        "last_seen": 123456789,
    }
    
    mock_prisma.device.find_unique = AsyncMock(return_value=existing_device)
    mock_prisma.device.update = AsyncMock(return_value=updated_device)

    command = UpsertDeviceCommand(
        device_id="test123",
        device_type="esp32",
        device_name="new_name",
        is_connected=True,
        last_seen=123456789,
    )

    # Act
    handler = create_upsert_device_command_handler(mock_prisma)
    result = await handler(command)

    # Assert
    mock_prisma.device.find_unique.assert_called_once_with(where={"id": "test123"})
    mock_prisma.device.update.assert_called_once_with(
        where={"id": "test123"},
        data={
            "is_connected": True,
            "last_seen": 123456789,
            "device_type": "esp32",
            "device_name": "new_name",
        }
    )
    assert result == updated_device
