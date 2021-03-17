import pytest
import event_processor
import json_schema


def test_validate_json_message_schema():
    expected = {'status': 'ok'}
    assert expected == json.loads(res.get_data(as_text=True))