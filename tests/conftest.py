import os
import boto3
import pytest
from moto import mock_aws

# Set dummy AWS credentials and region BEFORE any boto3-using code is imported.
# These satisfy boto3's construction requirements; moto intercepts real calls.
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "ap-south-1"

@pytest.fixture
def dynamodb_tables():
    """
    Starts the moto mock, creates both fake tables with the same schema
    as the real ones, seeds them, and yields so the test can run inside
    the mock. Everything after the yield is teardown.
    """
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")

        # Create the token-email-lookup table
        token_table = dynamodb.create_table(
            TableName='token-email-lookup',
            KeySchema=[{'AttributeName': 'token', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'token', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )

        # Create the user-notes table
        notes_table = dynamodb.create_table(
            TableName='user-notes',
            KeySchema=[{'AttributeName': 'user', 'KeyType': 'HASH'}, {'AttributeName': 'create_date', 'KeyType': 'RANGE'}],
            AttributeDefinitions=[{'AttributeName': 'user', 'AttributeType': 'S'}, {'AttributeName': 'create_date', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )

       # Seed the token-email-lookup table with a test token
        token_table.put_item(Item={"token": "abc123", "email": "alice@example.com"})
        token_table.put_item(Item={"token": "xyz789", "email": "bob@example.com"})

        # Seed the user-notes table with some test notes for Alice and Bob
        notes_table.put_item(Item={"user": "alice@example.com", "create_date": "2019-01-01T10:00:00Z", "id": "11111111-1111-4111-8111-111111111111", "text": "Alice buy groceries."})
        notes_table.put_item(Item={"user": "alice@example.com", "create_date": "2019-02-15T09:30:00Z", "id": "22222222-2222-4222-8222-222222222222", "text": "Alice call dentist."})
        notes_table.put_item(Item={"user": "alice@example.com", "create_date": "2019-03-20T14:00:00Z", "id": "33333333-3333-4333-8333-333333333333", "text": "Alice book flight tickets."})
        notes_table.put_item(Item={"user": "alice@example.com", "create_date": "2019-04-10T08:15:00Z", "id": "44444444-4444-4444-8444-444444444444", "text": "Alice renew gym membership."})
        notes_table.put_item(Item={"user": "bob@example.com", "create_date": "2019-01-01T10:00:00Z", "id": "55555555-5555-4555-8555-555555555555", "text": "Bob prepare presentation."})
        notes_table.put_item(Item={"user": "bob@example.com", "create_date": "2019-05-01T16:45:00Z", "id": "66666666-6666-4666-8666-666666666666", "text": "Bob file taxes."})

        yield dynamodb
