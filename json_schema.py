def get_base_message_schema():
    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'string'},
            'client_id': {'type': 'string'},
            'event_type': {'type': 'string'},
        },
        'required': ['id', 'client_id', 'event_type', 'payload']
    }

    return schema


def get_event_type_schema(event_type):
    if event_type == 'transaction':
        return get_schema_transaction()
    elif event_type == 'issue-credit-card':
        return get_schema_issue_credit_card()
    else:
        return ''


def get_schema_transaction():
    schema = {
        'type': 'object',
        'properties': {
            'credit_limit': {'type': 'number'},
            'processor': {'type': 'string'},
        },
        'required': ['credit_limit', 'processor']
    }

    return schema


def get_schema_issue_credit_card():
    schema = {
        'type': 'object',
        'properties': {
            'credit_limit': {'type': 'number'},
            'amount': {'type': 'number'},
        },
        'required': ['credit_limit', 'amount']
    }

    return schema
