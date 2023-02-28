from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dotorilocal

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/newquiz', methods=['GET'])
def newQuiz():
    return render_template("newquiz.html");

@app.route('/quizobj', methods=['GET'])
def quizObj():
    return render_template("quizobj.html");

@app.route('/quizsubj', methods=['GET'])
def quizSubj():
    return render_template("quizsubj.html");

if __name__ == '__main__':
    app.run(debug=True)
    