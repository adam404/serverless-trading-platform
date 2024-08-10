import json
from src.common.utils import get_table, response
from src.models.trade_models import MarketData

def process(event, context):
    """
    Process incoming market data and store in DynamoDB.
    """
    try:
        market_data = MarketData(**json.loads(event['body']))
        table = get_table('trading-table-' + context.function_name.split('-')[-1])
        
        table.put_item(Item=market_data.to_dict())
        
        return response(200, 'Market data processed successfully')
    except Exception as e:
        return response(500, f'Error processing market data: {str(e)}')