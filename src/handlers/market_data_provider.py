from abc import ABC, abstractmethod
from typing import Dict, Any

class MarketDataProvider(ABC):
    @abstractmethod
    def get_stock_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Dict[str, Any]:
        pass