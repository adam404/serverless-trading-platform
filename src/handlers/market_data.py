from typing import Dict, Any
from abc import ABC, abstractmethod
import yfinance as yf
from src.utils.helpers import get_table, create_response
from src.models import MarketData
from .yt_finance_provider import YFinanceProvider 

class MarketDataProvider(ABC):
    @abstractmethod
    def get_stock_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Dict[str, Any]:
        pass

# Remove the YFinanceProvider class from this file

def get_provider(provider_name: str) -> MarketDataProvider:
    providers = {
        'yfinance': YFinanceProvider(),
    }
    return providers.get(provider_name, YFinanceProvider())

def process(event, context):
    try:
        if 'body' not in event:
            return create_response(400, 'Missing request body')

        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return create_response(400, 'Invalid JSON in request body')

        if 'symbol' not in body:
            return create_response(400, 'Symbol is required')
        if 'timestamp' not in body:
            return create_response(400, 'Timestamp is required')

        symbol = body['symbol']
        timestamp = body['timestamp']
        provider_name = body.get('provider', 'yfinance')

        provider = get_provider(provider_name)
        stock_data = provider.get_stock_data(symbol)

        market_data = MarketData(
            symbol=symbol,
            timestamp=timestamp,
            price=stock_data['current_price'],
            change_percent=stock_data['change_percent'],
            high=stock_data['high'],
            low=stock_data['low'],
            volume=stock_data['volume']
        )

        table = get_table('market-data')
        table.put_item(Item=market_data.to_dict())
        
        return create_response(200, 'Market data processed successfully')
    except Exception as e:
        return create_response(500, f'Error processing market data: {str(e)}')