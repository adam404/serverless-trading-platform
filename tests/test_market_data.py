import json
import pytest
from src.handlers.market_data import process, YFinanceProvider
from unittest.mock import Mock
import yfinance as yf



from src.handlers.yt_finance_provider import YFinanceProvider
import yfinance as yf

def test_yfinance_provider(mocker):
    mock_ticker = mocker.Mock()
    mock_history = mocker.Mock()
    mock_close = mocker.Mock()
    mock_close.iloc = [150.00]
    mock_open = mocker.Mock()
    mock_open.iloc = [145.00]
    mock_history.__getitem__.side_effect = lambda x: {
        'Close': mock_close,
        'Open': mock_open,
        'High': mocker.Mock(max=lambda: 155.00),
        'Low': mocker.Mock(min=lambda: 145.00),
        'Volume': mocker.Mock(sum=lambda: 1000000)
    }[x]
    mock_ticker.history.return_value = mock_history
    mocker.patch('yfinance.Ticker', return_value=mock_ticker)

    provider = YFinanceProvider()
    data = provider.get_stock_data('AAPL')

    assert data['symbol'] == 'AAPL'
    assert data['current_price'] == 150.00
    assert isinstance(data['change_percent'], float)
    assert data['high'] == 155.00
    assert data['low'] == 145.00
    assert data['volume'] == 1000000

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

    assert result['statusCode'] == 400
    assert 'Invalid JSON in request body' in result['body']

def test_process_empty_event():
    event = {}
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})

    result = process(event, context)

    assert result['statusCode'] == 400
    assert 'Missing request body' in result['body']

def test_process_empty_event():
    event = {}
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})

    result = process(event, context)

    assert result['statusCode'] == 400
    assert 'Missing request body' in result['body']

def test_process_missing_timestamp():
    event = {
        'body': json.dumps({
            'symbol': 'AAPL'
        })
    }
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})

    result = process(event, context)

    assert result['statusCode'] == 400
    assert 'Timestamp is required' in result['body']

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
    assert 'Error processing market data: Database error' in result['body']


def test_process_invalid_provider(mocker):
    event = {
        'body': json.dumps({
            'symbol': 'AAPL',
            'timestamp': '2023-08-10T12:00:00Z',
            'provider': 'invalid_provider'
        })
    }
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})
    
    mocker.patch('src.handlers.market_data.get_table')
    mocker.patch('src.handlers.market_data.get_provider', return_value=mocker.Mock())
    
    result = process(event, context)
    
    assert result['statusCode'] == 200
    assert 'Market data processed successfully' in result['body']


def test_process_unexpected_error(mocker, mock_dynamodb_table):
    mocker.patch('src.handlers.market_data.get_provider', side_effect=Exception('Unexpected error'))
    event = {
        'body': json.dumps({
            'symbol': 'AAPL',
            'timestamp': '2023-08-10T12:00:00Z'
        })
    }
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})

    result = process(event, context)

    assert result['statusCode'] == 500
    assert 'Unexpected error' in result['body']

def test_yfinance_provider_error(mocker):
    mock_ticker = mocker.Mock()
    mock_ticker.history.side_effect = Exception('API Error')
    mocker.patch('yfinance.Ticker', return_value=mock_ticker)

    provider = YFinanceProvider()
    with pytest.raises(ValueError, match='Error fetching stock data: API Error'):
        provider.get_stock_data('AAPL')

def test_process_invalid_provider(mocker):
    event = {
        'body': json.dumps({
            'symbol': 'AAPL',
            'timestamp': '2023-08-10T12:00:00Z',
            'provider': 'invalid_provider'
        })
    }
    context = type('obj', (object,), {'function_name': 'processMarketData-dev'})
    
    mocker.patch('src.handlers.market_data.get_table')
    
    result = process(event, context)
    
    assert result['statusCode'] == 200
    assert 'Market data processed successfully' in result['body']

def test_get_provider():
    from src.handlers.market_data import get_provider
    from src.handlers.yt_finance_provider import YFinanceProvider

    provider = get_provider('yfinance')
    assert isinstance(provider, YFinanceProvider)

    provider = get_provider('unknown_provider')
    assert isinstance(provider, YFinanceProvider)


def test_get_provider():
    from src.handlers.market_data import get_provider
    from src.handlers.yt_finance_provider import YFinanceProvider

    provider = get_provider('yfinance')
    assert isinstance(provider, YFinanceProvider)

    provider = get_provider('unknown_provider')
    assert isinstance(provider, YFinanceProvider)