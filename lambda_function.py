import json

def lambda_handler(event, context):
    headers = event.get("headers") or {}
    lower_case = {k.lower(): v for k, v in headers.items()}
    auth_value = lower_case.get("authentication")
    if not auth_value:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing Authentication header"})}
    return {"statusCode": 200, "body": json.dumps({"header": lower_case['authentication']})}

if __name__ == "__main__":
    event = {"headers": {"Authentication": "Bearer abc123"}}
    print(lambda_handler(event, None))


