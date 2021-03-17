from flask import Flask
import event_processor
import time
import os
app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    return {'status': 'ok'}, 200


if __name__ == "__main__":
    print('DEBUG 0')
    event_processor.init_event_consuming()
    print('DEBUG 2')
    app.run(port=int(os.getenv('PORT')))
