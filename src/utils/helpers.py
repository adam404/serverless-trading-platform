import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

def get_table(table_name):
    """
    Get a DynamoDB table resource.
    """
    return dynamodb.Table(table_name)

def decimal_default(obj):
    """
    JSON encoder for Decimal objects.
    """
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def create_response(status_code: int, message: str, body: dict = None) -> dict:
    """
    Create a standardized API response.
    
    :param status_code: HTTP status code
    :param message: Response message
    :param body: Optional response body
    :return: Formatted response dictionary
    """
    response = {
        'statusCode': status_code,
        'body': json.dumps({'message': message, 'data': body} if body else {'message': message})
    }
    return response