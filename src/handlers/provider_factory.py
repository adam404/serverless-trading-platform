from .market_data_provider import MarketDataProvider
from .yfinance_provider import YFinanceProvider

def get_provider(provider_name: str) -> MarketDataProvider:
    providers = {
        'yfinance': YFinanceProvider(),
    }
    return providers.get(provider_name, YFinanceProvider())