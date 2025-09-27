
import requests
import os
import pytest

API_ENDPOINT_URL = os.environ.get("API_ENDPOINT_URL")

@pytest.mark.skipif(not API_ENDPOINT_URL, reason="API_ENDPOINT_URL environment variable not set")
def test_api_endpoint():
    """Tests the deployed API Gateway endpoint for a successful response."""
    payload = {
        "Pclass": 3,
        "Sex": "male",
        "Age": 22.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 7.25
    }

    headers = {"Content-Type": "application/json"}


    response = requests.post(API_ENDPOINT_URL, json=payload, headers=headers)
    response_data = response.json()


    assert response.status_code == 200, "API should return a 200 OK status"
    assert "prediction" in response_data, "Response JSON should contain a 'prediction' key"
    assert "interpretation" in response_data, "Response JSON should contain an 'interpretation' key"
    assert response_data["prediction"] in [0, 1], "Prediction value should be 0 or 1"