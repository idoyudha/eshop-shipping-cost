import json

# rate in usd per zipcode distance
RATE_PER_ZIPCODE = 100

def lambda_handler(event, context):
    try:
        print("Event:", event)

        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        print("Body:", body)

        from_zip = body['from_zip']
        to_zip = body['to_zip']

        if not from_zip or not to_zip:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Invalid zip codes: from_zip and to_zip are required'
                })
            }

        if int(to_zip) < int(from_zip):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Invalid zip codes: to_zip must be greater than from_zip'
                })
            }

        shipping_cost = calculate_shipping_cost(from_zip, to_zip)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'shipping_cost': shipping_cost,
                'message': 'Shipping cost calculated successfully'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': f'Missing required field: {str(e)}'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
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