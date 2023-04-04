from flask import Blueprint, g, render_template, request, url_for, session, redirect
from bson import ObjectId
import random
from bson import ObjectId

quiz_service = Blueprint("quiz_service", __name__)

###########################################
#
#
# 신규 퀴즈 출제 기능 구현: 이현지
#
#
###########################################
@quiz_service.route('/newquiz', methods=['GET', 'POST'])
def quizSubj():
    if request.method == "POST":
        question = request.form["question"]         # 문제
        answer = request.form["answer"]             # 정답
        explanation = request.form["explanation"]   # 해설
        madeBy = session["userid"]                  # 출제자
        
        # db에 신규 출제 문제 저장
        g.db.quizzes.insert_one({'objYN': 0, 'question': question, 'answer': answer, 'explanation': explanation, 'madeBy': madeBy});

        # 문제 출제자는 점수를 3점 올려준다
        dbuser = g.db.users.find_one({"userid": madeBy})
        prevPoint = dbuser["point"]

        g.db.users.update_one({'userid': madeBy}, {'$set': {'point': prevPoint + 3}})

        return redirect(url_for("profile"))
    
    else:
        return render_template("newquiz.html")

###########################################
#
#
# 출제한 퀴즈 리스트 조회 기능 구현: 이현지
#
#
###########################################
@quiz_service.route('/quizlist', methods=['GET'])
def quizlist():
    if request.method == "GET":
        # 1. 현재 사용자의 아이디를 가져온다
        currentid = session['userid']
        # 2. 현 사용자 아이디와 일치하는 문제들을 가져온다
        madequiz = list(g.db.quizzes.find({"madeBy": currentid}))
        # 3. 넘겨준다
        return render_template("quizlist.html", madequiz = madequiz)
    
###########################################
#
#
# 기존 출제 퀴즈 삭제 기능 구현: 이현지
#
#
###########################################
@quiz_service.route('/quizlist/delete', methods=['GET','POST'])
def quizdelete():
    if request.method == "POST":
        # 삭제하려는 해당 퀴즈의 id로 db에서 delete 한다
        qid = request.form["id"]
        g.db.quizzes.delete_one({'_id':ObjectId(qid)})
        return redirect(url_for("quizlist"))
    
    else:
        return render_template("quizlist.html")
    
###########################################
#
#
# 기존 출제 퀴즈 수정 기능 구현: 이현지
#
#
###########################################
@quiz_service.route('/quizlist/modify', methods=['GET','POST'])
def quizmodify():
    if request.method == "POST":
        qid = request.form["id"]                  # 퀴즈 Id
        question = request.form["question"]       # 문제
        answer = request.form["answer"]           # 정답
        explanation = request.form["explanation"] # 해설

        # db에 수정된 내용을 update 한다
        g.db.quizzes.update_one({'_id': ObjectId(qid)}, {'$set':{'question':question, 'answer': answer, 'explanation': explanation}})      
        
        return redirect(url_for("quiz_service.quizlist"))
    
    else:
        return render_template("quizlist.html")

###########################################
#
#
# 문제 은행 중 랜덤 5문제 추출 : 김재정
#
#
###########################################
@quiz_service.route('/descriptive',methods=['GET', 'POST'])
def descriptive():
    quiz_num=6
    set_question=[]
    # (난수값 생성)
    some_var = None
    random_numbers = random.sample(range(1,quiz_num), 5)
    randomddd=g.db.quizzes.aggregate([ { "$sample": { "size": 5 } }])
    
    select_quiz = []
    for x in randomddd:
        select_quiz.append(x)

    for i in range(len(random_numbers)) :
        quiz_set =g.db.quizzes.find_one({'qNnum':random_numbers[i]})
        set_question.insert(i, quiz_set)
    
    return render_template('descriptive.html',select_quiz=select_quiz)
    
###########################################
#
#
# 문제 풀이 중 오답처리 : 김재정
#
#
###########################################
@quiz_service.route('/descriptive_false/<quiz_id>')
def descriptive_false(quiz_id):
    # 오답 시 해당되는 퀴즈의 해설 페이지를 불러온다
    quiz_expl =g.db.quizzes.find_one({'_id': ObjectId(quiz_id)})

    return render_template('descriptive_false.html',quiz_id=quiz_id,quiz_expl=quiz_expl)

###########################################
#
#
# 전 문제 정답 시 처리 : 김재정
#
#
###########################################
@quiz_service.route('/success',methods=['GET', 'POST'])
def success():
    if request.method == "GET":
        solved_u = session["userid"]    # 사용자id
        dbuser = g.db.users.find_one({"userid": solved_u})
        prevPoint = dbuser["point"]     # 사용자 기존 점수

        # 5문제 세트 정답을 모두 맞추면 점수를 1점 올려준다
        g.db.users.update_one({'userid': solved_u}, {'$set': {'point': prevPoint + 1}})

        return render_template("success.html")
    
    else:
        return render_template("success.html")