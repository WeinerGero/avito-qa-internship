import pytest
import requests
import random
import string

BASE_URL = "https://qa-internship.avito.com"


# Create a random UUID for testing
@pytest.fixture
def seller_id():
    """_summary_

    Returns:
        _type_: _description_
    """
    return random.randint(111111, 999999)


# Create body for POST request for testing create item
@pytest.fixture
def item_body(seller_id):
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
    def test_create_item(self):
        pass

    def test_get_item_by_id(self):
        pass
        
    def test_get_items_by_seller_id(self):
        pass
    
    
    def test_get_statistic(self):
        pass
    
    
    def test_item_not_found(self):
        pass
    
    
