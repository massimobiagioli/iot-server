import pytest

from src.queries.find_device_query import create_find_device_query_handler


@pytest.mark.asyncio
async def test_find_device_query_handler_success(mock_prisma, a_device_query):
    expected_device = {"id": "1", "name": "Test Device"}
    mock_prisma.device.find_unique.return_value = expected_device

    handler = create_find_device_query_handler(mock_prisma)
    result = await handler(query=a_device_query)

    assert result == expected_device
    mock_prisma.device.find_unique.assert_called_once_with(where={"id": "dev123"})


@pytest.mark.asyncio
async def test_find_device_query_handler_not_found(mock_prisma, a_device_query):
    mock_prisma.device.find_unique.return_value = None

    handler = create_find_device_query_handler(mock_prisma)
    result = await handler(query=a_device_query)

    assert result is None
    mock_prisma.device.find_unique.assert_called_once_with(where={"id": "dev123"})
