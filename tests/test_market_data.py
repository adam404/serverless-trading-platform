import json
import pytest
from src.handlers.market_data import process, YFinanceProvider
from unittest.mock import Mock

@pytest.fixture
def mock_dynamodb_table(mocker):
    mock_table = mocker.Mock()
    mocker.patch('src.handlers.market_data.get_table', return_value=mock_table)
    return mock_table

@pytest.fixture
def mock_yfinance_provider(mocker):
    mock_provider = Mock(spec=YFinanceProvider)
    mock_provider.get_stock_data.return_value = {
        'symbol': 'AAPL',
        'current_price': 150.00,
        'change_percent': 1.5,
        'high': 155.00,
        'low': 145.00,
        'volume': 1000000
    }
    mocker.patch('src.handlers.market_data.get_provider', return_value=mock_provider)
    return mock_provider

def test_process_valid_market_data(mock_dynamodb_table, mock_yfinance_provider):
    event = {
        'body': json.dumps({
            'symbol': 'AAPL',
            'timestamp': '2023-08-10T12:00:00Z'
        })
    }
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})

    result = process(event, context)

    assert result['statusCode'] == 200
    assert 'Market data processed successfully' in result['body']
    mock_dynamodb_table.put_item.assert_called_once()

def test_process_invalid_json():
    event = {
        'body': 'Invalid JSON'
    }
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})

    result = process(event, context)

    assert result['statusCode'] == 400  # Changed from 500 to 400
    assert 'Invalid JSON in request body' in result['body']

def test_process_empty_event():
    event = {}
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})

    result = process(event, context)

    assert result['statusCode'] == 400  # Changed from 500 to 400
    assert 'Symbol is required' in result['body']

def test_process_provider_error(mock_yfinance_provider):
    mock_yfinance_provider.get_stock_data.side_effect = ValueError("API error")
    event = {
        'body': json.dumps({
            'symbol': 'AAPL',
            'timestamp': '2023-08-10T12:00:00Z'
        })
    }
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})

    result = process(event, context)

    assert result['statusCode'] == 400
    assert 'API error' in result['body']

def test_process_database_error(mock_dynamodb_table, mock_yfinance_provider):
    mock_dynamodb_table.put_item.side_effect = Exception("Database error")
    event = {
        'body': json.dumps({
            'symbol': 'AAPL',
            'timestamp': '2023-08-10T12:00:00Z'
        })
    }
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})

    result = process(event, context)

    assert result['statusCode'] == 500
    assert 'Error processing market data' in result['body']