from typing import Dict, Any
import yfinance as yf
from .market_data_provider import MarketDataProvider

class YFinanceProvider(MarketDataProvider):
    def get_stock_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Dict[str, Any]:
        try:
            stock = yf.Ticker(symbol)
            history = stock.history(period=period, interval=interval)
            
            return {
                'symbol': symbol,
                'current_price': float(history['Close'].iloc[-1]),
                'change_percent': float(((history['Close'].iloc[-1] - history['Open'].iloc[0]) / history['Open'].iloc[0]) * 100),
                'high': float(history['High'].max()),
                'low': float(history['Low'].min()),
                'volume': int(history['Volume'].sum())
            }
        except Exception as e:
            raise ValueError(f"Error fetching stock data: {str(e)}")