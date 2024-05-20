from flask import Flask,request,jsonify
from flask_cors import CORS
from recommendation import Recommendation
app = Flask(__name__)
CORS(app, supports_credentials=True)
recommendation=Recommendation()

@app.route('/signin', methods=['POST'])
def signin():
    return 'Welcome back!'

@app.route('/watched', methods=['POST'])
def watched():
    temp=request.json
    recommendation.addWatched(temp['user_id'],temp['anime_id'],temp['rating'])
    return 'Anime watched!'

@app.route('/signup', methods=['POST'])
def signup():
    temp=request.json
    user=recommendation.addUser(temp['name'])
    return jsonify(user)

@app.route('/recommend', methods=['POST'])
def recommend():
    temp=request.json
    ans=recommendation.recommend(temp['user_id'])
    return jsonify(ans)

if __name__ == '__main__':
    app.run(debug=True,port=4000)