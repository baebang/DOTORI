from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import random
app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.dotorilocal

        # question=quiz_set['question']
        # option1=quiz_set['option1']
        # option2=quiz_set['option2']
        # option3=quiz_set['option3']
        # option4=quiz_set['option4']
# HTML 화면 보여주기
@app.route('/',methods=['GET', 'POST'])
def home():
    # db 문제 길이를 함수에 저장
    quiz_num=6
    set_question=[]
    # # (난수값 생성)
    some_var = None
    random_numbers = random.sample(range(1,quiz_num), 5)

    if request.method == "POST":
        some_var = request.form.get('checks')
        # 유저에게 받은 값

    print("================random_numbers=",random_numbers)
    print("==========answer",some_var)

    for i in range(len(random_numbers)) :
    
        quiz_set =db.quizzes.find_one({'qNnum':random_numbers[i]})
        set_question.insert(i, quiz_set)

    
    return render_template('multiple_choice.html',set_question=set_question)

        

@app.route('/multiple_choice_false')
def fales():
    return render_template('multiple_choice_false.html')

@app.route('/descriptive')
def ddd():
    return render_template('descriptive.html')

@app.route('/descriptive_flase')
def descriptive_flase():
    return render_template('descriptive_flase.html')

@app.route('/success')
def sucess():
    return render_template('success.html')



# db.quizzes.insert_one({'qNnum': 1, 'question': "question", 'option1': "option1", 'option2': "option2", 'option3': "option3", 'option4': "option4",'answer': "answer", 'explanation': "explanation"});
# db.quizzes.insert_one({'qNnum':7,'objYN': 0, 'question': "question", 'answer': "answer", 'explanation': "explanation"});

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)