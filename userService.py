from flask import Blueprint, g, render_template, request, url_for, session, redirect, flash
import hashlib

user_service = Blueprint("user_service", __name__)

@user_service.route('/')
def index():
    if "userid" in session:
        sessionUser = g.db.users.find_one({"userid" : session["userid"]})
        return render_template('profile.html', loginUser = sessionUser)
    else:
        return render_template('index.html')

###########################################
#
#
# 회원가입 기능 구현: 조민기
#
#
###########################################
@user_service.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        nickname = request.form['nickname']
        userid = request.form['userid']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        member = {'username':username, 'nickname':nickname, 'userid':userid, 'password':password_hash, 'point':0}
        g.db.users.insert_one(member)

        return redirect(url_for("user_service.login"))
    
    else:
        return render_template('register.html')

###########################################
#
#
# 로그인 기능 구현: 조민기
#
#
###########################################
@user_service.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
        result = g.db.users.find_one({'userid': userid})
    
        if result is not None:
    
            if result['password'] == password_hash:
                session['userid'] = request.form['userid']
                return render_template('profile.html', loginUser = result)
                
            else:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect('/login')
        else:
            flash("아이디가 존재하지 않습니다.")
            return redirect('/login')
    else:
        return render_template('login.html')

###########################################
#
#
# 회원 프로필 조회 기능 구현: 조민기
#
#
###########################################
@user_service.route('/profile', methods=['GET'])
def profile():
    loggedin = g.db.users.find_one({'userid': session['userid']})

    return render_template('profile.html', loginUser = loggedin)

###########################################
#
#
# 회원 프로필 수정 기능 구현: 조민기
#
#
###########################################
@user_service.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if request.method == 'POST':        
        loggedin = g.db.users.find_one({"userid" : session['userid']})
        
        m_username = request.form['username']
        m_nickname = request.form['nickname']
        m_password = request.form['password']
        m_password_hash = hashlib.sha256(m_password.encode('utf-8')).hexdigest()
        
        g.db.users.update_one({'userid':session['userid']}, {'$set': {'username': m_username}})
        g.db.users.update_one({'userid':session['userid']}, {'$set': {'nickname': m_nickname}})
        g.db.users.update_one({'userid':session['userid']}, {'$set': {'password': m_password_hash}})

        return redirect(url_for('user_service.profile'))
    
    else:
        loggedin = g.db.users.find_one({"userid" : session['userid']})
        return render_template('editprofile.html', loginUser=loggedin)

###########################################
#
#
# 로그아웃 기능 구현: 조민기
#
#
###########################################
@user_service.route('/logout')
def logout():
    session.pop('userid', None)
    return render_template("index.html")