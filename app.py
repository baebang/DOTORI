from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dotorilocal

#db.quizzes.insert_one({'objYN': '객관식이면 1, 주관식이면 0', 'question':'문제', 'option1': 보기1', 'option2': '보기2', 'option3': '보기3', 'option4':'보기4', 'answer': '숫자(객관식) 아님 단답(주관식)', 'explanation': '해설', 'madeBy': '출제자id'});

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/newquiz', methods=['GET'])
def newQuiz():
    return render_template("newquiz.html");

# 객관식 문항 추가
@app.route('/quizobj', methods=['GET','POST'])
def quizObj():
    if request.method == "POST":
        question = request.form["question"]
        
        answer = request.form["answer"]
        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        option4 = request.form["option4"]
        answer = request.form["answer"]
        explanation = request.form["explanation"]

        #계정 연결되면 madeBy(문제 출제자 id 가져오기)도 추가가 되어야 함
        
        #madeBy = request.form["madeBy"]
        #db.quizzes.insert_one({'objYN': 0, 'question': question, 'answer': answer, 'explanation': explanation, 'madeBy': madeBy});
        
        db.quizzes.insert_one({'objYN': 0, 'question': question, 'option1': option1, 'option2': option2, 'option3': option3, 'option4': option4,'answer': answer, 'explanation': explanation});
        return redirect(url_for("index"))
    else:
      return render_template("quizobj.html");

# 주관식 문항 추가
@app.route('/quizsubj', methods=['GET', 'POST'])
def quizSubj():
    if request.method == "POST":
        question = request.form["question"]
        answer = request.form["answer"]
        explanation = request.form["explanation"]

        #계정 연결되면 madeBy(문제 출제자 id 가져오기)도 추가가 되어야 함
        
        #madeBy = request.form["madeBy"]
        #db.quizzes.insert_one({'objYN': 0, 'question': question, 'answer': answer, 'explanation': explanation, 'madeBy': madeBy});
        
        db.quizzes.insert_one({'objYN': 0, 'question': question, 'answer': answer, 'explanation': explanation});
        return redirect(url_for("index"))
    else:
      return render_template("quizsubj.html");

if __name__ == '__main__':
    app.run(debug=True)
    