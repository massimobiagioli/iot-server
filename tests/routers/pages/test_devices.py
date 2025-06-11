import pytest
from bs4 import BeautifulSoup


@pytest.mark.asyncio
async def test_index(async_client, create_device):
    device = await create_device()

    response = await async_client.get("/devices/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    soup = BeautifulSoup(response.text, "html.parser")

    tbody = soup.find("tbody")
    assert tbody is not None

    rows = tbody.find_all("tr")
    assert len(rows) == 1

    cells = rows[0].find_all("td")
    assert len(cells) == 4

    id_link = cells[0].find("a")
    assert id_link["href"] == f"/devices/{device.id}"
    assert id_link.string == str(device.id)

    assert cells[1].string == "Test Device"
    assert cells[2].string == "TEST"

    status_badge = cells[3].find("span")
    assert "badge" in status_badge["class"]
    assert "bg-secondary" in status_badge["class"]
    assert status_badge.string == "Disconnected"
