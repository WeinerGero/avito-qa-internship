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
    return {
        "sellerID": "<integer>",
        "name": "<string>",
        "price": "<integer>",
        "statistics": {
            "likes": "<integer>",
            "viewCount": "<integer>",
            "contacts": "<integer>"
        }
        }
