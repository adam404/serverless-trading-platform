import json
from src.common.utils import get_table, response
from src.models.trade_models import Trade

def execute(event, context):
    """
    Execute a trade based on the incoming trade signal.
    """
    try:
        trade = Trade(**json.loads(event['body']))
        table = get_table('trading-table-' + context.function_name.split('-')[-1])
        
        # Here you would typically interact with a trading API
        # For this example, we'll just store the trade in DynamoDB
        table.put_item(Item=trade.to_dict())
        
        return response(200, 'Trade executed successfully')
    except Exception as e:
        return response(500, f'Error executing trade: {str(e)}')