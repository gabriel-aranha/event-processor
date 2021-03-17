import pytest
import event_processor
import json_schema


def test_validate_json_base_schema_correct():
    json_message = {
        "id": "d19f29a0-9869-4bee-8651-8927520f2b6b",
        "client_id": "4414c8f0-b645-4bc5-9d78-1375c7ea159a",
        "event_type": "issue-credit-card",
        "payload": {
            "credit_limit": 2400,
            "processor": "MasterCard"
        }
    }

    base_validation_schema = json_schema.get_base_message_schema()
    base_result = event_processor.validate_json_message_schema(
        json_message, base_validation_schema)

    assert base_result == {'status': 'ok'}


def test_validate_json_base_schema_missing_key():
    json_message = {
        "id": "d19f29a0-9869-4bee-8651-8927520f2b6b",
        "client_id": "4414c8f0-b645-4bc5-9d78-1375c7ea159a",
        "payload": {
            "credit_limit": 2400,
            "processor": "MasterCard"
        }
    }

    base_validation_schema = json_schema.get_base_message_schema()
    base_result = event_processor.validate_json_message_schema(
        json_message, base_validation_schema)

    assert base_result['error']['message'] == "'event_type' is a required property"


def test_validate_json_base_schema_wrong_type():
    json_message = {
        "id": "d19f29a0-9869-4bee-8651-8927520f2b6b",
        "client_id": 555555555,
        "event_type": "issue-credit-card",
        "payload": {
            "credit_limit": 2400,
            "processor": "MasterCard"
        }
    }

    base_validation_schema = json_schema.get_base_message_schema()
    base_result = event_processor.validate_json_message_schema(
        json_message, base_validation_schema)

    assert base_result['error']['message'] == "555555555 is not of type 'string'"


def test_validate_json_payload_schema_correct_event():
    json_message = {
        "id": "d19f29a0-9869-4bee-8651-8927520f2b6b",
        "client_id": "4414c8f0-b645-4bc5-9d78-1375c7ea159a",
        "event_type": "issue-credit-card",
        "payload": {
            "credit_limit": 2400,
            "processor": "MasterCard"
        }
    }

    payload_validation_schema = json_schema.get_event_type_schema(
        'issue-credit-card')

    payload_result = event_processor.validate_json_message_schema(
        json_message['payload'], payload_validation_schema)

    assert payload_result == {'status': 'ok'}


def test_validate_json_payload_schema_wrong_event():
    json_message = {
        "id": "d19f29a0-9869-4bee-8651-8927520f2b6b",
        "client_id": "4414c8f0-b645-4bc5-9d78-1375c7ea159a",
        "event_type": "issue-credit-card",
        "payload": {
            "credit_limit": 2400,
            "processor": "MasterCard"
        }
    }

    payload_validation_schema = json_schema.get_event_type_schema(
        'transaction')

    payload_result = event_processor.validate_json_message_schema(
        json_message['payload'], payload_validation_schema)

    assert payload_result['error']['message'] == "'amount' is a required property"


def test_validate_json_payload_schema_missing_key():
    json_message = {
        "id": "d19f29a0-9869-4bee-8651-8927520f2b6b",
        "client_id": "4414c8f0-b645-4bc5-9d78-1375c7ea159a",
        "event_type": "issue-credit-card",
        "payload": {
            "processor": "MasterCard"
        }
    }

    payload_validation_schema = json_schema.get_event_type_schema(
        'issue-credit-card')

    payload_result = event_processor.validate_json_message_schema(
        json_message['payload'], payload_validation_schema)

    assert payload_result['error']['message'] == "'credit_limit' is a required property"


def test_validate_json_payload_schema_wrong_type():
    json_message = {
        "id": "d19f29a0-9869-4bee-8651-8927520f2b6b",
        "client_id": "4414c8f0-b645-4bc5-9d78-1375c7ea159a",
        "event_type": "issue-credit-card",
        "payload": {
            "credit_limit": "2400",
            "processor": "MasterCard"
        }
    }

    payload_validation_schema = json_schema.get_event_type_schema(
        'issue-credit-card')

    payload_result = event_processor.validate_json_message_schema(
        json_message['payload'], payload_validation_schema)

    assert payload_result['error']['message'] == "'2400' is not of type 'number'"
