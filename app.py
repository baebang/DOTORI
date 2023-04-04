from flask import Flask, current_app, g
from pymongo import MongoClient

from userService import user_service
from quizService import quiz_service
from rankingService import ranking_service

app = Flask(__name__)

SECRET_KEY = 'DOTORI'
app.secret_key = 'DOTORI'

# MongoDB 연결 설정
# 로컬환경 접속
client = MongoClient('localhost', 27017)
# AWS 접속
#client = MongoClient('mongodb://test:test@3.36.56.180', 27017)
db = client.dotorilocal
app.config['DB'] = db

# before_request 함수 등록
@app.before_request
def before_request():
    g.db = current_app.config['DB']

# Blueprint등록 
app.register_blueprint(user_service)
app.register_blueprint(quiz_service)
app.register_blueprint(ranking_service)

if __name__ == '__main__':  
    app.run('0.0.0.0',port=5000,debug=True)
