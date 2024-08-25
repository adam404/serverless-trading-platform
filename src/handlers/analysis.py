from src.utils.helpers import get_table, create_response
from src.models.trade_models import PerformanceMetrics
from decimal import Decimal

def perform_analysis():
    """
    Perform analysis and return metrics.
    """
    # Here you would typically perform your analysis
    # For this example, we'll just create dummy metrics
    return PerformanceMetrics(
        total_trades=100,
        winning_trades=60,
        total_profit=Decimal('1000.00')
    )

def perform(event, context):
    """
    Perform analysis on trading data and store results.
    """
    try:
        # Extract the environment from the function name
        function_name_parts = context.function_name.split('-')
        env = '-'.join(function_name_parts[1:])  # Join all parts after the first '-'
        table_name = f'trading-table-{env}'
        table = get_table(table_name)
        
        metrics = perform_analysis()
        
        # Convert Decimal to string for DynamoDB
        item = metrics.to_dict()
        item['total_profit'] = str(item['total_profit'])
        
        table.put_item(Item=item)
        
        return create_response(200, 'Analysis performed successfully')
    except Exception as e:
        return create_response(500, f'Error performing analysis: {str(e)}')