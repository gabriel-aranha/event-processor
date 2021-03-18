from jsonschema import validate, ValidationError, SchemaError
import json_schema
import pymongo
import pika
import json
import os


def init_event_consuming():
    url = os.getenv('RABBITMQ_CONN')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='events')

    channel.basic_consume(
        queue='events', on_message_callback=message_handler, auto_ack=True)

    channel.start_consuming()


def message_handler(ch, method, properties, body):
    validate_message(body)


def validate_message(message):
    json_message = load_message_into_json(message)

    base_validation_schema = json_schema.get_base_message_schema()

    base_result = validate_json_message_schema(
        json_message, base_validation_schema)

    message_id = get_message_id(json_message)

    if 'error' in base_result:
        if message_id != '':
            save_key_to_mongo(message_id, json_message)
            send_message('validation-error',
                         {'id': message_id, 'error': base_result['error']})
            return
        else:
            return

    message_event_type = get_message_event_type(json_message)
    if message_event_type == '':
        return

    payload_validation_schema = json_schema.get_event_type_schema(
        message_event_type)
    if payload_validation_schema == '':
        return

    payload_result = validate_json_message_schema(
        json_message['payload'], payload_validation_schema)

    if 'error' in payload_result:
        save_key_to_mongo(message_id, json_message)
        send_message('validation-error',
                     {'id': message_id, 'error': payload_result['error']})

    else:
        save_key_to_mongo(message_id, json_message)
        send_message('validation-success', {'id': message_id})


def save_key_to_mongo(key, payload):
    client = pymongo.MongoClient(os.getenv('MONGO_HOST'), username=os.getenv(
        'MONGO_USER'), password=os.getenv('MONGO_PASS'))
    events_db = client['events']
    messages_collection = events_db['messages']

    events_db.messages_collection.insert_one({'_id': key, 'message': payload})


def send_message(queue, message):
    url = os.getenv('RABBITMQ_CONN')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=json.dumps(message))

    connection.close()


def load_message_into_json(message):
    json_message = json.loads(message)

    return json_message


def validate_json_message_schema(message, schema):
    try:
        validate(message, schema)

        result = {
            'status': 'ok'
        }

        return result

    except SchemaError as e:
        error_result = {
            'message': e.message,
            'instance': e.instance,
        }

        result = {
            'error': error_result
        }

        return result

    except ValidationError as e:
        error_result = {
            'message': e.message,
            'instance': e.instance,
        }

        result = {
            'error': error_result
        }

        return result


def get_message_id(message):
    try:
        message_id = message['id']
        return message_id
    except:
        return ''


def get_message_event_type(message):
    try:
        message_event_type = message['event_type']
        return message_event_type
    except:
        return ''
