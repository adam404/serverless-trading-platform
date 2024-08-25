import pytest
from decimal import Decimal
from src.handlers.analysis import perform, perform_analysis
from src.models import PerformanceMetrics

@pytest.fixture
def mock_dynamodb_table(mocker):
    mock_table = mocker.Mock()
    mocker.patch('src.handlers.analysis.get_table', return_value=mock_table)
    return mock_table

@pytest.fixture
def mock_perform_analysis(mocker):
    mock_metrics = PerformanceMetrics(
        total_trades=100,
        winning_trades=60,
        total_profit=Decimal('1000.00')
    )
    mocker.patch('src.handlers.analysis.perform_analysis', return_value=mock_metrics)
    return mock_metrics

def test_perform_analysis():
    metrics = perform_analysis()
    assert isinstance(metrics, PerformanceMetrics)
    assert metrics.total_trades == 100
    assert metrics.winning_trades == 60
    assert metrics.total_profit == Decimal('1000.00')

def test_perform_success(mock_dynamodb_table, mock_perform_analysis):
    event = {}
    context = type('obj', (object,), {'function_name': 'analyzePerformance-dev'})

    result = perform(event, context)

    assert result['statusCode'] == 200
    assert 'Analysis performed successfully' in result['body']
    called_args = mock_dynamodb_table.put_item.call_args[1]['Item']
    assert isinstance(called_args['total_profit'], str)
    assert called_args['total_profit'] == '1000.00'

def test_perform_get_table_error(mocker):
    mocker.patch('src.handlers.analysis.get_table', side_effect=Exception('Database error'))
    
    event = {}
    context = type('obj', (object,), {'function_name': 'analyzePerformance-dev'})

    result = perform(event, context)

    assert result['statusCode'] == 500
    assert 'Error performing analysis: Database error' in result['body']

def test_perform_analysis_error(mocker, mock_dynamodb_table):
    mocker.patch('src.handlers.analysis.perform_analysis', side_effect=Exception('Analysis error'))
    
    event = {}
    context = type('obj', (object,), {'function_name': 'analyzePerformance-dev'})

    result = perform(event, context)

    assert result['statusCode'] == 500
    assert 'Error performing analysis: Analysis error' in result['body']

def test_perform_put_item_error(mock_dynamodb_table, mock_perform_analysis):
    mock_dynamodb_table.put_item.side_effect = Exception('Put item error')
    
    event = {}
    context = type('obj', (object,), {'function_name': 'analyzePerformance-dev'})

    result = perform(event, context)

    assert result['statusCode'] == 500
    assert 'Error performing analysis: Put item error' in result['body']

def test_perform_invalid_context():
    event = {}
    context = type('obj', (object,), {})  # context without function_name

    result = perform(event, context)

    assert result['statusCode'] == 500
    assert 'Error performing analysis' in result['body']

def test_perform_create_response_error(mocker, mock_dynamodb_table, mock_perform_analysis):
    mocker.patch('src.handlers.analysis.create_response', side_effect=Exception('Response error'))
    
    event = {}
    context = type('obj', (object,), {'function_name': 'analyzePerformance-dev'})

    with pytest.raises(Exception) as excinfo:
        perform(event, context)
    
    assert str(excinfo.value) == 'Response error'

def test_perform_function_name_splitting(mocker, mock_perform_analysis):
    mock_get_table = mocker.patch('src.handlers.analysis.get_table')
    mock_table = mocker.Mock()
    mock_get_table.return_value = mock_table

    event = {}
    context = type('obj', (object,), {'function_name': 'analyzePerformance-test-env-prod'})

    result = perform(event, context)

    assert result['statusCode'] == 200
    mock_get_table.assert_called_once()
    mock_table.put_item.assert_called_once()
    
    # Check if 'test-env-prod' is in the table name
    table_name = mock_get_table.call_args[0][0]
    assert 'trading-table-test-env-prod' == table_name

    # Verify that the correct item was put into the table
    put_item_args = mock_table.put_item.call_args[1]['Item']
    assert 'total_trades' in put_item_args
    assert 'winning_trades' in put_item_args
    assert 'total_profit' in put_item_args
    assert isinstance(put_item_args['total_profit'], str)