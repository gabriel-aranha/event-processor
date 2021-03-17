from flask import Flask
import event_processor
import time
import os
app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    return {'status': 'ok'}, 200


@app.route('/activate', methods=['GET'])
def activate_processor():
    event_processor.init_event_consuming()
    return {'status': 'ok'}, 200


if __name__ == "__main__":
    if os.getenv('CLOUD'):
        time.sleep(60)
    event_processor.init_event_consuming()
    app.run(port=int(os.getenv('PORT')))