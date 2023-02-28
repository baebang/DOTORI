from flask import Flask, render_template, request, jsonify, url_for, session, redirect, flash
from pymongo import MongoClient
import hashlib, datetime, jwt

client = MongoClient('localhost', 27017)
db = client.db_dotori


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
    
        member = {'username':username, 'nickname':nickname, 'userid':userid, 'password':password_hash}
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
                payload = {
                'id': userid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                #return jsonify({'result': 'success', 'token': token})
                return render_template('success.html')
                
            else:
                flash("비밀번호가 일치하지 않습니다.")
                return render_template('login.html')
        else:
            flash("아이디가 존재하지 않습니다.")
            return render_template('login.html')
    else:
        return render_template('login.html')



if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)