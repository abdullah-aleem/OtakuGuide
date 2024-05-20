from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/signin', methods=['POST'])
def signin():
    return 'Welcome back!'


@app.route('/signup', methods=['POST'])
def signup():
    return 'Welcome!'

@app.route('/recommend', methods=['POST'])
def recommend():
    return 'Recommendation!'

if __name__ == '__main__':
    app.run(debug=True,port=4000)