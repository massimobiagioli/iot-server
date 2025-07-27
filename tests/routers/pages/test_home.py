import pytest


@pytest.mark.asyncio
async def test_home(
    async_client,
):
    response = await async_client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "This is the home page of your IoT server" in response.text

    # Check for device statistics widget
    assert "Total Devices" in response.text
    assert "Connected" in response.text
    assert "Disconnected" in response.text

    # Check for FontAwesome icons
    assert "fa-microchip" in response.text
    assert "fa-wifi" in response.text
    assert "fa-unlink" in response.text
