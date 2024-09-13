from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class MarketData:
    symbol: str
    price: Decimal
    timestamp: str

    def to_dict(self):
        return {k: str(v) if isinstance(v, (datetime, Decimal)) else v 
                for k, v in asdict(self).items()}

@dataclass
class Trade:
    symbol: str
    quantity: int
    price: Decimal
    timestamp: datetime
    action: str  # 'BUY' or 'SELL'

    def to_dict(self):
        return {k: str(v) if isinstance(v, (datetime, Decimal)) else v 
                for k, v in asdict(self).items()}

@dataclass
class PerformanceMetrics:
    total_trades: int
    winning_trades: int
    total_profit: Decimal

    def to_dict(self):
        return {k: str(v) if isinstance(v, Decimal) else v 
                for k, v in asdict(self).items()}
    
