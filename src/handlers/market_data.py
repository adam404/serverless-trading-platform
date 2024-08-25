import json
from typing import Dict, Any
from abc import ABC, abstractmethod
import yfinance as yf
from src.utils.helpers import get_table, create_response
from src.models import MarketData

class MarketDataProvider(ABC):
    @abstractmethod
    def get_stock_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Dict[str, Any]:
        pass

# Make sure to update the YFinanceProvider class to use 'symbol' instead of 'ticker'
class YFinanceProvider(MarketDataProvider):
    def get_stock_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Dict[str, Any]:
        try:
            stock = yf.Ticker(symbol)
            history = stock.history(period=period, interval=interval)
            
            return {
                'symbol': symbol,
                'current_price': history['Close'].iloc[-1],
                'change_percent': ((history['Close'].iloc[-1] - history['Open'].iloc[0]) / history['Open'].iloc[0]) * 100,
                'high': history['High'].max(),
                'low': history['Low'].min(),
                'volume': history['Volume'].sum()
            }
        except Exception as e:
            raise ValueError(f"Error fetching stock data: {str(e)}")

def get_provider(provider_name: str) -> MarketDataProvider:
    providers = {
        'yfinance': YFinanceProvider(),
        # Add more providers here as needed
    }
    return providers.get(provider_name, YFinanceProvider())  # Default to YFinanceProvider

def process(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Process incoming market data request, fetch data from provider, and store in DynamoDB.
    """
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return create_response(400, 'Invalid JSON in request body')

    symbol = body.get('symbol')
    provider_name = body.get('provider', 'yfinance')
    
    if not symbol:
        return create_response(400, 'Symbol is required')
    
    try:
        provider = get_provider(provider_name)
        market_data = provider.get_stock_data(symbol)
        
        # Convert market_data to MarketData model
        market_data_model = MarketData(
            symbol=market_data['symbol'],
            price=market_data['current_price'],
            timestamp=body.get('timestamp', '')  # You might want to generate a timestamp if not provided
        )
        
        table = get_table('trading-table-' + context.function_name.split('-')[-1])
        table.put_item(Item=market_data_model.to_dict())
        
        return create_response(200, 'Market data processed successfully', market_data_model.to_dict())
    except ValueError as ve:
        return create_response(400, str(ve))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Add this line for debugging
        return create_response(500, f'Error processing market data: {str(e)}')
