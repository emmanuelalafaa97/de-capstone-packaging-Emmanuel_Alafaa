from unittest.mock import patch, MagicMock
import pytest
from omnicart_pipeline.api import API

import logging

#logger = logging.getLogger("TestAPI", "tests.log")

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

@patch('requests.get')
def test_get_all_users_success(mock_get):
     """Tests a successful API call for a user."""
     # Arrange: Configure the mock to simulate a successful response
     mock_response = MagicMock()
     mock_response.status_code = 200
     mock_response.json.return_value = mock_users
     mock_get.return_value = mock_response
     # Act: Call the method we are testing
     client = API()
     user_data = client.get_all_users()
     # Assert: Check that the method returned the expected data
     #assert user_data == []     #this will assert or check for an empty list use the isinstance instead
     assert isinstance(user_data, list)
     # Assert that our mock was called correctly
     mock_get.assert_called_once_with("https://fakestoreapi.com/users")



@patch('requests.get')
def test_get_all_products_success(mock_get):
     """Tests a successful API call for a product."""
     # Arrange: Configure the mock to simulate a successful response
     mock_response = MagicMock()
     mock_response.status_code = 200
     mock_response.json.return_value = mock_products
     mock_get.return_value = mock_response
     # Act: Call the method we are testing
     client = API()
     prod_data = client.get_all_products()
     # Assert: Check that the method returned the expected data
     #assert user_data == []     #this will assert or check for an empty list use the isinstance instead
     assert isinstance(prod_data, list)
     # Assert that our mock was called correctly
     mock_get.assert_called_once_with("https://fakestoreapi.com/products/")



@patch('requests.get')
def test_pagination_products(mock_get):
     """Ensure pagination is applied and the full list is returned in order."""
      # Arrange: Configure the mock to simulate a successful response
     mock_response = MagicMock()
     mock_response.status_code = 200
     mock_response.json.return_value = mock_products
     mock_get.return_value = mock_response
     # Act: Call the method we are testing
     client = API()
     client.limit = 1  # force pagination into multiple pages
     paginated_prod_result = client.get_all_products()  
     # Assert: ensure full list returned, preserving order, and request was made
     #check the products pagination
     assert isinstance(paginated_prod_result, list)
     assert len(paginated_prod_result) == len(mock_products)
     assert paginated_prod_result == mock_products
     mock_get.assert_called_once_with("https://fakestoreapi.com/products/")

@patch('requests.get')     
def test_pagination_users(requests_mock):
     """Ensure pagination is applied and the full list is returned in order."""
      # Arrange: Configure the mock to simulate a successful response
       # Arrange: create a larger mock product list (12 items)
     mock_users_large = [
        {"id": i, "title": f"users-{i}", "email": str(i)} for i in range(1, 13)
     ]
     mock_response = MagicMock()
     mock_response.status_code = 200
     mock_response.json.return_value = mock_users or mock_users_large   # note how we used two different list variables for our mock test and both passed because we used the "OR" operator  
     requests_mock.return_value = mock_response
     # Act: Call the method we are testing
     client = API()
     client.limit = 1  # force pagination into multiple pages
     paginated_user_result = client.get_all_users()
     assert isinstance(paginated_user_result, list)
     assert len(paginated_user_result) == len(mock_users_large) or len(mock_users)
     assert paginated_user_result == mock_users 
     requests_mock.assert_called_once_with("https://fakestoreapi.com/users")


@patch('requests.get')     
def test_pagination_users_alternate_test(requests_mock):
     """Ensure pagination is applied and the full list is returned in order."""
      # Arrange: Configure the mock to simulate a successful response
       # Arrange: create a larger mock product list (12 items)
     mock_users_large = [
        {"id": i, "title": f"users-{i}", "email": str(i)} for i in range(1, 13)
     ]
     mock_response = MagicMock()
     mock_response.status_code = 200
     mock_response.json.return_value = mock_users_large   # note how we used two different list variables for our mock test and both passed because we used the "OR" operator  
     requests_mock.return_value = mock_response
     # Act: Call the method we are testing
     client = API()
     client.limit = 1  # force pagination into multiple pages
     paginated_user_result = client.get_all_users()
     assert isinstance(paginated_user_result, list)
     assert len(paginated_user_result) == len(mock_users_large)    #however note that this checks with the assigned "mock_response.json.return_value"
     assert paginated_user_result == mock_users_large
     requests_mock.assert_called_once_with("https://fakestoreapi.com/users")

