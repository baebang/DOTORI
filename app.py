from flask import Flask, render_template, request, jsonify, url_for, session, redirect, flash
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import hashlib, datetime, jwt

client = MongoClient('localhost', 27017)
db = client.dotorilocal

app = Flask(__name__)

SECRET_KEY = 'DOTORI'
app.secret_key = 'DOTORI'

### 추후 계정 연결 시 수정해야 되는 부분
TEST_MADEBY_ID = 'test'

# index 페이지
@app.route('/')
def index():
    return render_template('index.html')


###########################################
#
#
# 로그인 기능 구현: 조민기
#
#
###########################################
    

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        nickname = request.form['nickname']
        userid = request.form['userid']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        #f = request.files['ex_file']
        #f.save(secure_filename(f.filename))
        
        member = {'username':username, 'nickname':nickname, 'userid':userid, 'password':password_hash, 'point':0}
        db.users.insert_one(member)

        return redirect(url_for("login"))
    
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
        result = db.users.find_one({'userid': userid})
    
        if result is not None:
    
            if result['password'] == password_hash:
                # payload = {
                # 'id': userid,
                # 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
                # }
                # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                session['loginFlag'] = True
                session['userid'] = userid
                # 랭킹을 변수로 가져가기 위해 수정해야 하는 부분
                return render_template('profile.html', loginUser = result)
                # return jsonify({'result': 'success', 'token': token})
                
            else:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect('/login')
        else:
            flash("아이디가 존재하지 않습니다.")
            return redirect('/login')
    else:
        return render_template('login.html')
    
@app.route('/profile', methods=['GET'])
def profile():
    
    return render_template('profile.html')


@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if request.method == 'POST':
        return redirect('/profile')
    else:
        return render_template('editprofile.html')

# 토큰 삭제가 안됨!!!
@app.route('/logout')
def logout():
    # token_receive = request.cookies.get('token')
    # payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    session.pop('userid', None)
    return redirect(url_for('/'))


###########################################
#
#
# 퀴즈 출제 기능 구현: 이현지
#
#
###########################################
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
        db.quizzes.insert_one({'objYN': 1, 'question': question, 'option1': option1, 'option2': option2, 'option3': option3, 'option4': option4,'answer': answer, 'explanation': explanation, 'madeBy': TEST_MADEBY_ID});
        
        # 문제 출제자는 점수를 3점 올려준다
        dbuser = db.users.find_one({"userid": TEST_MADEBY_ID})
        prevPoint = dbuser["point"]

        db.users.update_one({'userid': TEST_MADEBY_ID}, {'$set': {'point': prevPoint + 3}})

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
        
        db.quizzes.insert_one({'objYN': 0, 'question': question, 'answer': answer, 'explanation': explanation, 'madeBy': TEST_MADEBY_ID});

        # 문제 출제자는 점수를 3점 올려준다
        dbuser = db.users.find_one({"userid": TEST_MADEBY_ID})
        prevPoint = dbuser["point"]

        db.users.update_one({'userid': TEST_MADEBY_ID}, {'$set': {'point': prevPoint + 3}})

        return redirect(url_for("index"))
    else:
        return render_template("quizsubj.html")

@app.route('/quizlist', methods=['GET'])
# 퀴즈 조회, 퀴즈 업데이트, 퀴즈 삭제
def quizlist():
    if request.method == "GET":
        # 1. 현재 사용자의 아이디를 가져온다
        currentid = 'test'
        # 2. 현 사용자 아이디와 일치하는 문제들을 가져온다
        madequiz = list(db.quizzes.find({"madeBy": currentid}))
        # 3. 넘겨준다
        return render_template("quizlist.html", madequiz = madequiz)
    
@app.route('/quizlist/delete', methods=['GET','POST'])
def quizdelete():
    if request.method == "POST":
        question = request.form('question')
        deletequiz = db.quizzes.find_one({'question': question})
        return redirect(url_for("quizlist"))
    else:
        return render_template("quizlist.html")

@app.route('/quizlist/modify/<id>', methods=['GET','POST'])
def quizmodify():
    question = request.values.get('question')
    if request.method == "POST":
        return redirect(url_for("quizlist"))
    else:
        return render_template("quizlist.html")


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)