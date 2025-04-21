# test_app.py
from fastapi.testclient import TestClient
from unittest import mock

# Import your FastAPI app - assuming your file is named main.py
# If it's named differently, change this import
from backend.main import app

# Create test client
client = TestClient(app)

def test_currency_conversion():
    """Test the currency conversion endpoint works correctly"""
    
    # Create a mock response that mimics what the external API would return
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "query": {
            "from": "USD",
            "to": "EUR",
            "amount": 100
        },
        "info": {
            "rate": 0.85
        },
        "result": 85.0
    }
    
    # Mock the async httpx get method to avoid real API calls
    async def mock_get(*args, **kwargs):
        return mock_response
    
    # Apply our mock during the test
    with mock.patch('httpx.AsyncClient.get', side_effect=mock_get):
        # Send a test request to our endpoint
        response = client.post(
            "/convert",
            json={"from_currency": "USD", "to_currency": "EUR", "amount": 100}
        )
        
        # Check the response status code is OK
        assert response.status_code == 200
        
        # Check we got the expected data back
        data = response.json()
        assert "converted_amount" in data
        assert data["converted_amount"] == 85.0  # Should be rounded to 2 decimal places
# Add these tests to your test_app.py file

def test_root_endpoint():
    """Test the root endpoint returns the expected message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Currency Converter (Live Rates)"}

def test_symbols_endpoint_success():
    """Test the symbols endpoint returns currency symbols correctly"""
    # Mock response for currency symbols
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "symbols": {
            "USD": "United States Dollar",
            "EUR": "Euro",
            "GBP": "British Pound Sterling"
        }
    }
    
    async def mock_get(*args, **kwargs):
        return mock_response
    
    with mock.patch('httpx.AsyncClient.get', side_effect=mock_get):
        response = client.get("/symbols")
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "symbols" in data
        assert "USD" in data["symbols"]

def test_symbols_endpoint_failure():
    """Test error handling when symbols API call fails"""
    mock_response = mock.MagicMock()
    mock_response.status_code = 400
    
    async def mock_get(*args, **kwargs):
        return mock_response
    
    with mock.patch('httpx.AsyncClient.get', side_effect=mock_get):
        response = client.get("/symbols")
        
        assert response.status_code == 400
        assert "detail" in response.json()

def test_conversion_invalid_currency():
    """Test error handling for invalid currency codes"""
    # Mock an API response indicating failure due to invalid currency
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": False,
        "error": {
            "code": "invalid_currency_code",
            "message": "Invalid currency code"
        }
    }
    
    async def mock_get(*args, **kwargs):
        return mock_response
    
    with mock.patch('httpx.AsyncClient.get', side_effect=mock_get):
        response = client.post(
            "/convert",
            json={"from_currency": "INVALID", "to_currency": "EUR", "amount": 100}
        )
        
        assert response.status_code == 400
        assert "detail" in response.json()

def test_conversion_api_failure():
    """Test error handling when conversion API call fails"""
    mock_response = mock.MagicMock()
    mock_response.status_code = 500
    
    async def mock_get(*args, **kwargs):
        return mock_response
    
    with mock.patch('httpx.AsyncClient.get', side_effect=mock_get):
        response = client.post(
            "/convert",
            json={"from_currency": "USD", "to_currency": "EUR", "amount": 100}
        )
        
        assert response.status_code == 500
        assert "detail" in response.json()

def test_conversion_different_currencies():
    """Test currency conversion with different currency pairs"""
    # Test JPY to GBP conversion
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "query": {
            "from": "JPY",
            "to": "GBP",
            "amount": 10000
        },
        "info": {
            "rate": 0.0055
        },
        "result": 55.0
    }
    
    async def mock_get(*args, **kwargs):
        return mock_response
    
    with mock.patch('httpx.AsyncClient.get', side_effect=mock_get):
        response = client.post(
            "/convert",
            json={"from_currency": "JPY", "to_currency": "GBP", "amount": 10000}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["converted_amount"] == 55.0

