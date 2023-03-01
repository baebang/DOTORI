from flask import Flask, render_template, request, jsonify, url_for, session, redirect, flash
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import hashlib, datetime, jwt

client = MongoClient('localhost', 27017)
db = client.dotorilocal


app = Flask(__name__)

SECRET_KEY = 'DOTORI'
app.secret_key = 'DOTORI'

# index 페이지
@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        nickname = request.form['nickname']
        userid = request.form['userid']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        f = request.files['ex_file']
        f.save(secure_filename(f.filename))
        
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


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)