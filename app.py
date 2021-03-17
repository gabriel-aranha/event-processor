from flask import Flask
import event_processor
import time
import os
app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    return {'status': 'ok'}, 200


if __name__ == "__main__":
    time.sleep(10)
    event_processor.init_event_consuming()
    app.run(port=os.getenv('PORT'))
