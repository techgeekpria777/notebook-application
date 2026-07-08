import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
token_table = dynamodb.Table('token-email-lookup')
notes_table = dynamodb.Table('user-notes')

def _json_default(obj):
    if isinstance(obj, Decimal):
        # convert to int if it's a whole number, else float
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def lambda_handler(event, context):
    headers = event.get("headers") or {}
    lower_case = {k.lower(): v for k, v in headers.items()}
    auth_value = (lower_case.get("authentication"))
    if not auth_value:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing Authentication header"})}
    parts = auth_value.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return {"statusCode": 400, "body": json.dumps({"error": "Malformed Authentication header"})}
    token = parts[1]
    token_response = token_table.get_item(Key={"token": token})
    if 'Item' not in token_response:
        return {"statusCode": 403, "body": json.dumps({"error": "Forbidden Request"})}
    email = token_response['Item']['email']
    notes_response = notes_table.query(
        KeyConditionExpression=Key('user').eq(email),
        ScanIndexForward=False,
        Limit=10
    )
    items = notes_response.get('Items', [])
    return {"statusCode": 200, "body": json.dumps({"notes": items}, default=_json_default)}

if __name__ == "__main__":
    test_cases = [
        {"headers": {"Authentication": "Bearer abc123"}},
        {"headers": {"Authentication": "Bearer   abc123"}},
        {"headers": {"Authentication": "  bearer abc123  "}},
        {"headers": {"Authentication": "Bearer"}},
        {"headers": {"Authentication": "Basic abc123"}},
        {"headers": {"Authentication": "abc123"}},
        {"headers": {}},
        {"headers": None},
        {"headers": {"Authentication":"Bearer xyz789"}},
        {"headers": {"Authentication":"Bearer doesnotexist"}}
    ]
    for event in test_cases:
        print(lambda_handler(event, None))


