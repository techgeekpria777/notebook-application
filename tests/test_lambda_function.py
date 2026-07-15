def test_valid_tokens_return_notes(dynamodb_tables):
    import json

    from lambda_function import lambda_handler

    event = {"headers": {"Authentication": "Bearer abc123"}}
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    notes = body["notes"]

    # Alice has 4 notes
    assert len(notes) == 4
    # newest first: 2019-04-10 should be the first note
    assert notes[0]["create_date"] == "2019-04-10T08:15:00Z"
    # oldest last
    assert notes[-1]["create_date"] == "2019-01-01T10:00:00Z"

def test_invalid_token_returns_403(dynamodb_tables):
    import json

    from lambda_function import lambda_handler

    event = {"headers": {"Authentication": "Bearer doesnotexist"}}
    response = lambda_handler(event, None)
    assert response["statusCode"] == 403
    body = json.loads(response["body"])
    assert body["error"] == "Forbidden Request"

def test_missing_header_returns_400(dynamodb_tables):
    import json

    from lambda_function import lambda_handler

    event = {"headers": {}}
    response = lambda_handler(event, None)
    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["error"] == "Missing Authentication header"

def test_null_headers_returns_400(dynamodb_tables):
    import json

    from lambda_function import lambda_handler

    event = {"headers": None}
    response = lambda_handler(event, None)
    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["error"] == "Missing Authentication header"

def test_malformed_header_returns_400(dynamodb_tables):
    import json

    from lambda_function import lambda_handler

    event = {"headers": {"Authentication":  "Basic abc123"}}
    response = lambda_handler(event, None) 
    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["error"] == "Malformed Authentication header"

def test_bearer_case_insensitive(dynamodb_tables):
    import json

    from lambda_function import lambda_handler

    event = {"headers": {"Authentication": "bearer abc123"}}
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    notes = body["notes"]
    assert len(notes) == 4
    assert notes[0]["create_date"] == "2019-04-10T08:15:00Z"
    assert notes[-1]["create_date"] == "2019-01-01T10:00:00Z"

def test_user_isolation(dynamodb_tables):
    #event with Bob's token "Bearer xyz789", assert 200, assert exactly 2 notes, and assert every returned note's user is bob@example.com 
    import json

    from lambda_function import lambda_handler

    event = {"headers": {"Authentication": "Bearer xyz789"}}
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    notes = body["notes"]
    assert len(notes) == 2
    assert all(note["user"] == "bob@example.com" for note in notes)