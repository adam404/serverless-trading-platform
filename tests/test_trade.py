import pytest
from src.handlers.trade import execute
from src.models.trade_models import Trade
from decimal import Decimal
from datetime import datetime
import json

@pytest.fixture
def mock_dynamodb_table(mocker):
    mock_table = mocker.Mock()
    mocker.patch('src.handlers.trade.get_table', return_value=mock_table)
    return mock_table

def test_execute_valid_trade(mock_dynamodb_table):
    event = {
        'body': json.dumps({
            'symbol': 'AAPL',
            'quantity': 10,
            'price': '150.00',
            'timestamp': '2023-08-10T12:00:00Z',
            'action': 'BUY'
        })
    }
    context = type('obj', (object,), {'function_name': 'executeTradeStrategy-dev'})

    result = execute(event, context)

    assert result['statusCode'] == 200
    assert 'Trade executed successfully' in result['body']
    mock_dynamodb_table.put_item.assert_called_once()

def test_execute_invalid_trade():
    event = {
        'body': json.dumps({
            'symbol': 'AAPL'  # Missing required fields
        })
    }
    context = type('obj', (object,), {'function_name': 'executeTradeStrategy-dev'})

    result = execute(event, context)

    assert result['statusCode'] == 500
    assert 'Error executing trade' in result['body']

def test_execute_invalid_json():
    event = {
        'body': 'Invalid JSON'
    }
    context = type('obj', (object,), {'function_name': 'executeTradeStrategy-dev'})

    result = execute(event, context)

    assert result['statusCode'] == 500
    assert 'Error executing trade' in result['body']

def test_execute_database_error(mocker):
    mocker.patch('src.handlers.trade.get_table', side_effect=Exception('Database error'))
    event = {
        'body': json.dumps({
            'symbol': 'AAPL',
            'quantity': 10,
            'price': '150.00',
            'timestamp': '2023-08-10T12:00:00Z',
            'action': 'BUY'
        })
    }
    context = type('obj', (object,), {'function_name': 'executeTradeStrategy-dev'})

    result = execute(event, context)

    assert result['statusCode'] == 500
    assert 'Error executing trade' in result['body']