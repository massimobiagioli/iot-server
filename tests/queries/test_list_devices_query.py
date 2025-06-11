import pytest

from src.queries.list_devices_query import create_list_devices_query_handler


@pytest.mark.asyncio
async def test_list_devices_query_handler_success(mock_prisma):
    expected_devices = [{"id": "1", "name": "Test Device"}]
    mock_prisma.device.find_many.return_value = expected_devices

    handler = create_list_devices_query_handler(mock_prisma)
    result = await handler()

    assert result == expected_devices
    mock_prisma.device.find_many.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_devices_query_handler_empty(mock_prisma):
    mock_prisma.device.find_many.return_value = []

    handler = create_list_devices_query_handler(mock_prisma)
    result = await handler()

    assert result == []
    mock_prisma.device.find_many.assert_awaited_once()
