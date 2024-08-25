import json
from typing import Dict, Any
from src.utils.helpers import get_table, create_response
from src.models import MarketData

def process(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Process incoming market data and store in DynamoDB.
    """
    try:
        # For scheduled events, we might need to fetch market data from an external API here
        # For this example, we'll assume the data is passed in the event
        market_data = MarketData(**json.loads(event.get('body', '{}')))
        table = get_table('trading-table-' + context.function_name.split('-')[-1])
        
        table.put_item(Item=market_data.to_dict())
        
        return create_response(200, 'Market data processed successfully')
    except Exception as e:
        return create_response(500, f'Error processing market data: {str(e)}')