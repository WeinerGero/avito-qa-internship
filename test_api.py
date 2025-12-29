import pytest
import requests
import random
from typing import Any, Dict
import re

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


# Create an item and return its ID for testing get item by ID
@pytest.fixture
def created_item(item_body):
    """
    Create an item and return its ID for testing get item by ID.
    
    :param item_body: Description
    """
    url = f"{BASE_URL}/api/1/item"
    response = requests.post(url, json=item_body)
    response.raise_for_status()
    
    resp_json = response.json()
    
    if "id" in resp_json:
        return resp_json["id"]
    
    if "status" in resp_json:
        status_text = resp_json["status"]
        match = re.search(r'[a-f0-9\-]{36}', status_text)
        if match:
            return match.group(0)
            
    return None



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

    def test_get_item_by_id(self, item_body, created_item):
        """
        The second test case. Get ad by ID (GET).
        
        :param item_body: Description
        :param created_item: Description
        """

        item_id = created_item
        assert item_id is not None, "Failed to create item for setup"

        url = f"{BASE_URL}/api/1/item/{item_id}"
        response = requests.get(url)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        if isinstance(data, list):
            item_data = data[0]
        else:
            item_data = data

        assert item_data["id"] == item_id
        assert item_data["sellerId"] == item_body["sellerID"]
        assert item_data["name"] == item_body["name"]
        assert item_data["price"] == item_body["price"]


    def test_get_items_by_seller_id(self, seller_id, item_body):
        """
        The third test case. Get all ads by sellerID (GET).
        
        :param seller_id: Description
        :param item_body: Description
        """

        requests.post(f"{BASE_URL}/api/1/item", json=item_body)
        
        body_2 = item_body.copy()
        body_2["name"] = "Товар 2"
        requests.post(f"{BASE_URL}/api/1/item", json=body_2)

        url = f"{BASE_URL}/api/1/{seller_id}/item"
        response = requests.get(url)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        items = response.json()
        
        assert isinstance(items, list), f"Expected list, got {type(items)}"
        
        assert len(items) >= 2, "Expected at least 2 items for this seller"
        
        for item in items:
            assert item["sellerId"] == seller_id, \
                f"Item belongs to wrong seller: {item['sellerId']}"
            
            assert "id" in item, "Item missing 'id'"
            assert "createdAt" in item, "Item missing 'createdAt'"
            assert "name" in item, "Item missing 'name'"
            assert "price" in item, "Item missing 'price'"
            
            assert "statistics" in item, "Item missing 'statistics'"
            stats = item["statistics"]
            assert "likes" in stats
            assert "viewCount" in stats
            assert "contacts" in stats

    def test_get_statistic(self, item_body, created_item):
        """
        The fourth test case. Get statistics for an ad (GET).
        
        :param item_body: Description
        :param created_item: Description
        """
        item_id = created_item
        url = f"{BASE_URL}/api/1/statistic/{item_id}"
        
        response = requests.get(url)
        assert response.status_code == 200
        
        stats = response.json()
        
        if isinstance(stats, list):
            stats = stats[0]
            
        assert stats["likes"] == item_body["statistics"]["likes"]
        assert stats["viewCount"] == item_body["statistics"]["viewCount"]
        assert stats["contacts"] == item_body["statistics"]["contacts"]

    def test_create_item_invalid_price(self, seller_id):
        """
        The fifth test case. Negative test case. Create with invalid price.
        
        :param seller_id: Description
        """
        body = {
            "sellerID": seller_id,
            "name": "Bad Price Item",
            "price": -100,  # Error
            "statistics": {}
        }
        
        url = f"{BASE_URL}/api/1/item"
        response = requests.post(url, json=body)
        
        assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"

    def test_get_non_existent_item(self):
        """
        The sixth test case. Negative test. Requesting a non-existent ID.
        """
        # create a fake UUID
        fake_id = "00000000-0000-0000-0000-000000000000"
        url = f"{BASE_URL}/api/1/item/{fake_id}"
        
        response = requests.get(url)
        
        assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}"
