import pytest
from bs4 import BeautifulSoup


@pytest.mark.asyncio
async def test_get_device(async_client, create_device):
    device = await create_device(is_connected=True)

    response = await async_client.get(f"/devices/{device.id}")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="table")
    assert table is not None

    rows = table.find("tbody").find_all("tr")
    assert len(rows) == 4

    def get_row_values(row):
        cells = row.find_all("td")
        return {
            "label": cells[0].get_text(strip=True),
            "value": cells[1].get_text(strip=True) if len(cells) > 1 else None,
            "element": cells[1] if len(cells) > 1 else None,
        }

    id_row = get_row_values(rows[0])
    assert id_row["label"] == "ID"
    assert id_row["value"] == device.id

    name_row = get_row_values(rows[1])
    assert name_row["label"] == "Display Name"
    assert name_row["value"] == device.display_name

    family_row = get_row_values(rows[2])
    assert family_row["label"] == "Family"
    assert family_row["value"] == device.family
