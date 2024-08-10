import pytest
from src.functions.market_data import process
from src.models.trade_models import MarketData
from decimal import Decimal
from datetime import datetime

def test_process_market_data():
    event = {
        'body': '{"symbol": "AAPL", "price": "150.00", "timestamp": "2023-08-10T12:00:00Z"}'
    }
    context = type('obj', (object,), {'function_name': 'market-data-dev'})

    result = process(event, context)

    assert result['statusCode'] == 200
    assert 'Market data processed successfully' in result['body']

def test_process_invalid_market_data():
    event = {
        'body': '{"symbol": "AAPL"}'  # Missing required fields
    }
    context = type('obj', (object,), {'function_name': 'market-data-dev'})

    result = process(event, context)

    assert result['statusCode'] == 500
    assert 'Error processing market data' in result['body']