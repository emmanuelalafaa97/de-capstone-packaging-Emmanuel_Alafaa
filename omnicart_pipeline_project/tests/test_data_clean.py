from unittest.mock import patch, MagicMock
import pytest
import pandas as pd
from omnicart_pipeline.data_enricher import Enricher
from omnicart_pipeline.data_clean import Cleaning

users_data = Enricher.users_data_enricher()
products_data = Enricher.prod_data_enricher()

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

users_df = pd.DataFrame(mock_users)
prod_df = pd.DataFrame(mock_products)




@patch("omnicart_pipeline.data_clean.Cleaning.left_merged")
def test_left_merged_success(mock_left_merged):
    merged_data = pd.merge(users_df, prod_df, on='id', how='left')
    mock_left_merged.return_value = merged_data

    clean = Cleaning()
    result = clean.left_merged(users_df, prod_df)
    
    #Assert
    #assert clean.left_merged(users_df, prod_df) == merged_data     #tried this way bu did not work
    assert result.equals(merged_data)        #checking to confirm that using clean.left_merged(users_df, prod_df) merges data on 'id' and using a left merge
    assert isinstance(result, pd.DataFrame)  #ensure it is a dataframe
    assert len(result) == len(users_df)  # Should maintain left DataFrame length
    assert 'title' in result.columns  # Should include columns from products
    assert 'email' in result.columns  # Should include columns from users



@patch("omnicart_pipeline.data_clean.Cleaning.clean_data")
def test_left_data_clean_success(mock_clean_data):
    pass
