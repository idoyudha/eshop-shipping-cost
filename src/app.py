import json
from http import HTTPStatus

# rate in usd per zipcode distance
RATE_PER_ZIPCODE = 2

def lambda_handler(event, context):
    try:
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})

        from_zip = body['from_zip']
        to_zip = body['to_zip']

        if not from_zip or not to_zip:
            return {
                'statusCode': HTTPStatus.BAD_REQUEST,
                'body': json.dumps({
                    'message': 'Invalid zip codes: from_zip and to_zip are required'
                })
            }

        shipping_cost = calculate_shipping_cost(from_zip, to_zip)

        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps({
                'code': 200,
                'data': {
                    'shipping_cost': shipping_cost,
                },
                'message': 'Shipping cost calculated successfully'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    
    except KeyError as e:
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': json.dumps({
                'message': f'Missing required field: {str(e)}'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({
                'message': 'Internal server error'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

def calculate_shipping_cost(from_zip: str, to_zip: str) -> float:
    """Calculate shipping cost between two zip codes"""
    return RATE_PER_ZIPCODE * abs(int(from_zip) - int(to_zip) + 1)