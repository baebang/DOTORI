from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dotorilocal

# id, name, profile, pw, nickname, point
#db.users.insert_one({'name': '이현지', 'nickname':'hj', 'point': 5});
#db.users.insert_one({'name': '김재정', 'nickname':'jj', 'point': 10});
#db.users.insert_one({'name': '조민기', 'nickname':'mg', 'point': 15});

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ranking', methods=['GET'])
def ranking():
    #1. db에 저장된 명단을 가져온다(point 높은 순으로 정렬한다)
    userslist = list(db.users.find({}, {'_id':False}).sort('point', -1))

    return render_template("ranking.html", userslist = userslist)


if __name__ == '__main__':
    app.run(debug=True)
    