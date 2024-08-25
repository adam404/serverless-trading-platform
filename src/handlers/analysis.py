from src.utils.helpers import get_table, create_response
from src.models.trade_models import PerformanceMetrics

def perform(event, context):
    """
    Perform analysis on trading data and store results.
    """
    try:
        table = get_table('trading-table-' + context.function_name.split('-')[-1])
        
        # Here you would typically perform your analysis
        # For this example, we'll just create dummy metrics
        metrics = PerformanceMetrics(
            total_trades=100,
            winning_trades=60,
            total_profit=1000.00
        )
        
        table.put_item(Item=metrics.to_dict())
        
        return create_response(200, 'Analysis performed successfully')
    except Exception as e:
        return create_response(500, f'Error performing analysis: {str(e)}')