from unittest.mock import AsyncMock, Mock

import pytest
from httpx import ASGITransport, AsyncClient

from prisma import Prisma
from src import prisma
from src.main import app
from src.queries.find_device_query import FindDeviceQuery


@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(autouse=True)
async def prisma_connection():
    if not prisma.is_connected():
        await prisma.connect()

    yield

    if prisma.is_connected():
        await prisma.disconnect()


@pytest.fixture
def mock_prisma():
    prisma = Mock(spec=Prisma)
    prisma.device = Mock()
    prisma.device.find_many = AsyncMock()
    prisma.device.find_unique = AsyncMock()
    return prisma


@pytest.fixture
def a_device_query() -> FindDeviceQuery:
    return FindDeviceQuery(device_id="dev123")


@pytest.fixture
async def create_device():
    devices_created = []

    async def _create_device(
        device_id: str = "test-device-123",
        device_type: str = "esp32",
        device_name: str = "test-device",
        is_connected: bool = False,
        last_seen: int = None,
    ):
        device = await prisma.device.create(
            data={
                "id": device_id,
                "device_type": device_type,
                "device_name": device_name,
                "is_connected": is_connected,
                "last_seen": last_seen,
            }
        )

        devices_created.append(device.id)
        return device

    yield _create_device

    for device_id in devices_created:
        await prisma.device.delete(where={"id": device_id})
