from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import random
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dotorilocal

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/descriptive',methods=['GET', 'POST'])
def descriptive():
    quiz_num=6
    set_question=[]
    # (난수값 생성)
    some_var = None
    random_numbers = random.sample(range(1,quiz_num), 5)


    print("================random_numbers=",random_numbers)
    print("==========answer",some_var)

    for i in range(len(random_numbers)) :
    
        quiz_set =db.quizzes.find_one({'qNnum':random_numbers[i]})
        set_question.insert(i, quiz_set)

    
    return render_template('descriptive.html',set_question=set_question)
    

@app.route('/descriptive_false')
def descriptive_flase():
    return render_template('descriptive_false.html')

@app.route('/success')
def sucess():
    return render_template('success.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)