import pytest
from bs4 import BeautifulSoup


@pytest.mark.asyncio
async def test_index(async_client, create_device):
    device = await create_device(
        device_id="test-device-123",
        device_type="esp32",
        device_name="test-device",
        is_connected=False,
        last_seen=1234567890,
    )

    response = await async_client.get("/devices/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    # Check that the page contains the device management card
    soup = BeautifulSoup(response.text, "html.parser")

    # Check for the main card structure
    card = soup.find("div", class_="card")
    assert card is not None

    # Check for the card header with title
    card_header = card.find("div", class_="card-header")
    assert card_header is not None
    assert "Device Management" in card_header.get_text()

    # Check for the table structure
    table = soup.find("table", id="devicesTable")
    assert table is not None

    # Check table headers
    headers = table.find("thead").find_all("th")
    expected_headers = ["Device ID", "Name", "Type", "Status", "Last Seen", "Actions"]
    for i, expected_header in enumerate(expected_headers):
        assert expected_header in headers[i].get_text()

    # Check that JavaScript data is embedded
    script_tags = soup.find_all("script")
    device_data_found = False
    for script in script_tags:
        if script.string and "devicesData" in script.string:
            device_data_found = True
            # Check that device data contains our test device
            assert device.id in script.string
            assert "esp32" in script.string
            break

    assert device_data_found, "Device data not found in JavaScript"
