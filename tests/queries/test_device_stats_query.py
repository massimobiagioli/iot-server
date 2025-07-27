from unittest.mock import AsyncMock

import pytest

from src.queries.device_stats_query import create_device_stats_query_handler


@pytest.mark.asyncio
async def test_device_stats_query_handler_success():
    # Arrange
    mock_prisma = AsyncMock()
    mock_prisma.device.count.side_effect = [5, 3]  # total=5, connected=3
    
    handler = create_device_stats_query_handler(mock_prisma)
    
    # Act
    result = await handler()
    
    # Assert
    assert result == {
        "total": 5,
        "connected": 3,
        "disconnected": 2
    }
    
    # Verify calls
    assert mock_prisma.device.count.call_count == 2
    mock_prisma.device.count.assert_any_call()  # First call without where
    mock_prisma.device.count.assert_any_call(where={"is_connected": True})  # Second call with where


@pytest.mark.asyncio
async def test_device_stats_query_handler_empty():
    # Arrange
    mock_prisma = AsyncMock()
    mock_prisma.device.count.side_effect = [0, 0]  # total=0, connected=0
    
    handler = create_device_stats_query_handler(mock_prisma)
    
    # Act
    result = await handler()
    
    # Assert
    assert result == {
        "total": 0,
        "connected": 0,
        "disconnected": 0
    }


@pytest.mark.asyncio
async def test_device_stats_query_handler_all_connected():
    # Arrange
    mock_prisma = AsyncMock()
    mock_prisma.device.count.side_effect = [3, 3]  # total=3, connected=3
    
    handler = create_device_stats_query_handler(mock_prisma)
    
    # Act
    result = await handler()
    
    # Assert
    assert result == {
        "total": 3,
        "connected": 3,
        "disconnected": 0
    }


@pytest.mark.asyncio
async def test_device_stats_query_handler_all_disconnected():
    # Arrange
    mock_prisma = AsyncMock()
    mock_prisma.device.count.side_effect = [4, 0]  # total=4, connected=0
    
    handler = create_device_stats_query_handler(mock_prisma)
    
    # Act
    result = await handler()
    
    # Assert
    assert result == {
        "total": 4,
        "connected": 0,
        "disconnected": 4
    }
