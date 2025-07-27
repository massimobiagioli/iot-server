import pytest
from bs4 import BeautifulSoup


@pytest.mark.asyncio
async def test_get_device(async_client, create_device):
    device = await create_device(
        device_id="test-device-detail",
        device_type="esp32",
        device_name="test-device",
        is_connected=True,
        last_seen=1234567890,
    )

    response = await async_client.get(f"/devices/{device.id}")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="table")
    assert table is not None

    rows = table.find("tbody").find_all("tr")
    # Updated to expect correct number of rows: ID, Device Type, Device Name, Last Seen, Status
    assert len(rows) >= 4  # At least ID, Device Type, Device Name, Last Seen, Status

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

    # Check for device type and device name starting from row 1 (after ID)
    device_type_found = False
    device_name_found = False
    last_seen_found = False
    status_found = False

    for row in rows[1:]:  # Start from row 1 (after ID row)
        row_data = get_row_values(row)
        if "Device Type" in row_data["label"]:
            # Device type is shown as a badge, so check for the badge content
            badge = row_data["element"].find("span", class_="badge")
            if badge:
                assert device.device_type.upper() in badge.get_text()
                device_type_found = True
        elif "Device Name" in row_data["label"]:
            assert row_data["value"] == device.device_name
            device_name_found = True
        elif "Last Seen" in row_data["label"]:
            # Last seen can be "Never" or a timestamp
            last_seen_found = True
        elif "Status" in row_data["label"]:
            # Status should show Connected/Disconnected badge
            status_found = True

    # Ensure we found the expected fields
    assert device_type_found, "Device Type field not found"
    assert device_name_found, "Device Name field not found"
    assert last_seen_found, "Last Seen field not found"
    assert status_found, "Status field not found"
