import pytest
from src.handlers.provider_factory import get_provider
from src.handlers.yt_finance_provider import YFinanceProvider

def test_get_provider():
    provider = get_provider('yfinance')
    assert isinstance(provider, YFinanceProvider)