from unittest.mock import patch, MagicMock
import pytest
from omnicart_pipeline.data_enricher import Enricher
import pandas as pd
from omnicart_pipeline.api import API


mock_users = [
    {
        'id': 1,
        'email': 'john@gmail.com',
        'username': 'johnd',
        'name': {'firstname': 'john', 'lastname': 'doe'},
        'phone': '1-570-236-7033',
        'address': {'city': 'kilcoole'}
    },
    {
        'id': 2,
        'email': 'morrison@gmail.com',
        'username': 'mor_2314',
        'name': {'firstname': 'david', 'lastname': 'morrison'},
        'phone': '1-570-236-7033',
        'address': {'city': 'kilcoole'}
    }
]

 # Sample mock data
mock_products = [
    {
        'id': 1,
        'title': 'Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops',
        'price': 109.95,
        'category': "men's clothing",
        'rating': {'rate': 3.9, 'count': 120}
    },
    {
        'id': 2,
        'title': 'Mens Casual Premium Slim Fit T-Shirts',
        'price': 22.3,
        'category': "men's clothing",
        'rating': {'rate': 4.1, 'count': 259}
    }
]

mock_users_df = pd.DataFrame(mock_users)
mock_products_df = pd.DataFrame(mock_products)


@patch("omnicart_pipeline.data_enricher.API.get_all_users")
def test_users_enricher_success(requests_mock):
    mock_response = MagicMock()
    mock_response.status_code = 200
    #mock_response.json.return_value = mock_users
    mock_response.DataFrame.return_value = mock_users
    requests_mock.return_value = mock_response
    # This is the beginning of the main test from the real file
    user_data = Enricher.users_data_enricher()
    # Assert: Check that the method returned the expected data
    assert isinstance(user_data, pd.DataFrame)    # if you put "list" or anything else that does not follow with the value of Enricher.users_data_enricher() it would throw up false
    
@patch("omnicart_pipeline.data_enricher.API.get_all_products") #pay attention to this file patch names and path too
def test_products_enricher_success(requests_mock):
    mock_response = MagicMock()
    mock_response.status_code = 200
    #mock_response.json.return_value = mock_products
    mock_response.DataFrame.return_value = mock_products_df   #note the mock tests mock_products or mock_products_df both pass
    requests_mock.return_value = mock_response
    # This is the beginning of the main test from the real file
    prod_data = Enricher.prod_data_enricher()
    # Assert: Check that the method returned the expected data
    assert isinstance(prod_data, pd.DataFrame) 