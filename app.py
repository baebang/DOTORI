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
@app.route('/',methods=['GET','POST'])
def home():
    # # db 문제 길이를 함수에 저장
    quiz_num=6
    # # (난수값 생성)
    # random_numbers = random.sample(range(1,quiz_num), 5)
    quiz_set =db.quizzes.find_one({'qNnum':5})

    if request.method == "POST":
        some_var = request.form.get('checks')
        # 유저에게 받은 값
    print(quiz_set)   
    return render_template("multiple_choice.html", quiz_set = quiz_set)
    
    
    


    # for i in random_numbers:
    #     # 숫자에 맞는 퀴즈를 가져온다 'qNnum':2 << 이 번호를 random_numbers[1]
    #     quiz_set =db.quizzes.find_one({'qNnum':random_numbers[i]})
    #     if some_var == quiz_set['answer']:
    #          quiz_set =db.quizzes.find_one({'qNnum':random_numbers[i+1]})
    #          return render_template('multiple_choice.html',quiz_set )
    #     else:
    #         return redirect(url_for("descriptive_flase"))

        


        # 유저가 정답에 맞는 버튼을 누를경우 킵고잉
        # 틀릴경우 일단 fales 화면으로 이동

    # return render_template('multiple_choice.html')

        

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