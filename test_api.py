import pytest
import requests
import random
import string
from typing import Any, Dict

BASE_URL = "https://qa-internship.avito.com"


# Create a random UUID for testing
@pytest.fixture
def seller_id() -> int:
    """_summary_

    Returns:
        _type_: _description_
    """
    return random.randint(111111, 999999)


# Create body for POST request for testing create item
@pytest.fixture
def item_body(seller_id) -> Dict[str, Any]:
    """
    Docstring for item_body
    
    :param seller_id: Description
    :return: Description
    :rtype: dict[str, Any]
    """
    return {
        "sellerID": seller_id,
        "name": "Товар",
        "price": random.randint(10, 10_000),
        "statistics": {
            "likes": random.randint(0, 100),
            "viewCount": random.randint(0, 1000),
            "contacts": random.randint(0, 10)
        }
    }


class TestAvitoAPI:
    
    def test_create_item(self, item_body):
        """
        The first test case. Register a new ad (POST).
        
        :param item_body: Description
        """

        url = f"{BASE_URL}/api/1/item"
        response = requests.post(url, json=item_body)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        resp_data = response.json()

        assert "status" in resp_data or "id" in resp_data, "Response should contain 'status' or 'id'"



