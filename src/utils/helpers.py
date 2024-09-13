import json
import boto3
from decimal import Decimal
from typing import Union, Dict, Any

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

def create_response(status_code: int, body: Union[str, Dict, Exception]) -> Dict[str, Any]:
    if isinstance(body, Exception):
        message = str(body)
    elif isinstance(body, dict):
        message = json.dumps(body, default=decimal_default)
    else:
        message = body
    return {
        'statusCode': status_code,
        'body': json.dumps({'message': message})
    }