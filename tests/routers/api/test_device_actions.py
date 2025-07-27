import json
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


@patch('src.routers.api.device_actions.mqtt')
def test_ping_device_success(mock_mqtt, client):
    """Test successful device ping"""
    # Mock MQTT client
    mock_mqtt.client.publish = AsyncMock()
    
    # Make request
    response = client.post("/api/devices/test-device-123/ping")
    
    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Ping sent to device test-device-123"
    assert data["topic"] == "outbound/test-device-123"
    assert "payload" in data
    assert data["payload"]["command"] == "ping"
    assert "timestamp" in data["payload"]
    assert data["payload"]["payload"] == {}
    
    # Verify MQTT publish was called
    mock_mqtt.client.publish.assert_called_once()
    call_args = mock_mqtt.client.publish.call_args
    assert call_args[0][0] == "outbound/test-device-123"  # topic
    assert call_args[1]["qos"] == 1  # qos parameter
    
    # Verify message format
    published_message = call_args[0][1].decode("utf-8")
    message_data = json.loads(published_message)
    assert message_data["command"] == "ping"
    assert message_data["payload"] == {}
    assert "timestamp" in message_data


@patch('src.routers.api.device_actions.mqtt')
def test_ping_device_mqtt_error(mock_mqtt, client):
    """Test device ping with MQTT error"""
    # Mock MQTT client to raise exception
    mock_mqtt.client.publish.side_effect = Exception("MQTT connection failed")
    
    # Make request
    response = client.post("/api/devices/test-device-456/ping")
    
    # Verify error response
    assert response.status_code == 500
    data = response.json()
    assert "Failed to send ping to device test-device-456" in data["detail"]
    assert "MQTT connection failed" in data["detail"]


def test_ping_device_invalid_method(client):
    """Test ping endpoint with invalid HTTP method"""
    response = client.get("/api/devices/test-device/ping")
    assert response.status_code == 405  # Method Not Allowed


@patch('src.routers.api.device_actions.mqtt')
def test_ping_device_with_special_characters(mock_mqtt, client):
    """Test device ping with special characters in device ID"""
    # Mock MQTT client
    mock_mqtt.client.publish = AsyncMock()
    
    device_id = "device-with-special_chars.123"
    response = client.post(f"/api/devices/{device_id}/ping")
    
    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["topic"] == f"outbound/{device_id}"
    
    # Verify MQTT publish was called with correct topic
    mock_mqtt.client.publish.assert_called_once()
    call_args = mock_mqtt.client.publish.call_args
    assert call_args[0][0] == f"outbound/{device_id}"
