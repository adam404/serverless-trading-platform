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

def create_response(status_code, body):
    """
    Create a standardized response object.
    """
    return {
        'statusCode': status_code,
        'body': json.dumps(body, default=decimal_default)
    }