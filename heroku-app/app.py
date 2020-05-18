from flask import Flask, request, jsonify
from scheduling import run
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/schedule/', methods=['GET'])
def respond():
    return ''

@app.route('/schedule/', methods=['POST'])
def post_something():
    courses     = request.form.get('courses')
    preferences = request.form.get('preferences')

    result = run(courses, preferences)

    return result

# A welcome message to test our server
@app.route('/')
def index():
    return ''

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
