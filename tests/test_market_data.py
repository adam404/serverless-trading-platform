import pytest
from src.handlers.market_data import process
from src.models.trade_models import MarketData
from decimal import Decimal
from datetime import datetime
import json
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_dynamodb_table(mocker):
    mock_table = mocker.Mock()
    mocker.patch('src.handlers.market_data.get_table', return_value=mock_table)
    return mock_table

def test_process_valid_market_data(mock_dynamodb_table):
    event = {
        'body': json.dumps({
            'symbol': 'AAPL',
            'price': '150.00',
            'timestamp': '2023-08-10T12:00:00Z'
        })
    }
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})

    result = process(event, context)

    assert result['statusCode'] == 200
    assert 'Market data processed successfully' in result['body']
    mock_dynamodb_table.put_item.assert_called_once()

def test_process_invalid_market_data():
    event = {
        'body': json.dumps({
            'symbol': 'AAPL'  # Missing required fields
        })
    }
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})

    result = process(event, context)

    assert result['statusCode'] == 500
    assert 'Error processing market data' in result['body']