from src.utils.helpers import create_response, get_table
import json
import pytest

def test_create_response():
    response = create_response(200, 'Success')
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == {'message': 'Success'}

    response = create_response(500, 'Internal Server Error')
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == {'message': 'Internal Server Error'}

def test_create_response_with_exception():
    response = create_response(500, Exception('Test exception'))
    assert response['statusCode'] == 500
    body = json.loads(response['body'])
    assert body['message'] == 'Test exception'

def test_create_response_with_dict():
    response = create_response(200, {'key': 'value'})
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == {'message': '{"key": "value"}'}

def test_create_response_with_string():
    response = create_response(400, 'Error message')
    assert response['statusCode'] == 400
    assert json.loads(response['body']) == {'message': 'Error message'}

def test_create_response_with_none():
    response = create_response(204, None)
    assert response['statusCode'] == 204
    assert json.loads(response['body']) == {'message': None}

def test_get_table():
    table = get_table('test-table')
    assert table.name == 'test-table'

def test_create_response_with_dict():
    response = create_response(200, {'key': 'value'})
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == {'message': '{"key": "value"}'}

def test_decimal_default():
    from decimal import Decimal
    from src.utils.helpers import decimal_default

    assert decimal_default(Decimal('10.5')) == 10.5

    with pytest.raises(TypeError):
        decimal_default('not a decimal')