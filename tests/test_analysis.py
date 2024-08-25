import pytest
from src.handlers.analysis import perform
from src.models.trade_models import PerformanceMetrics
from decimal import Decimal

def test_perform_analysis(mocker):
    mock_table = mocker.Mock()
    mocker.patch('src.handlers.analysis.get_table', return_value=mock_table)

    event = {}
    context = type('obj', (object,), {'function_name': 'analyzePerformance-dev'})

    result = perform(event, context)

    assert result['statusCode'] == 200
    assert 'Analysis performed successfully' in result['body']
    mock_table.put_item.assert_called_once()

def test_perform_analysis_error(mocker):
    mocker.patch('src.handlers.analysis.get_table', side_effect=Exception('Database error'))
    
    event = {}
    context = type('obj', (object,), {'function_name': 'analyzePerformance-dev'})

    result = perform(event, context)

    assert result['statusCode'] == 500
    assert 'Error performing analysis' in result['body']