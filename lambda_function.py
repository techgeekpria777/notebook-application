import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('token-email-lookup')

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
    response = table.get_item(Key={"token": token})
    if 'Item' not in response:
        return {"statusCode": 403, "body": json.dumps({"error": "Forbidden Request"})}
    return {"statusCode": 200, "body": json.dumps({"email": response['Item']['email']})}

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


