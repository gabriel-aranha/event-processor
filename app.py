from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    return {'status': 'ok'}, 200


if __name__ == "__main__":
    app.run()
