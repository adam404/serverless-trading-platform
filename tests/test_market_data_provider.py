import pytest
from src.handlers.market_data_provider import MarketDataProvider
from src.handlers.yt_finance_provider import YFinanceProvider

def test_market_data_provider():
    provider = YFinanceProvider()
    assert isinstance(provider, MarketDataProvider)
    
    # Test that the method is implemented
    assert hasattr(provider, 'get_stock_data')
    assert callable(getattr(provider, 'get_stock_data'))
