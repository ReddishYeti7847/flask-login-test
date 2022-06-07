import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, redirect
from werkzeug.security import generate_password_hash
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:256UniA:fsP4@localhost/スケジュール'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
 
login_manager = LoginManager()
login_manager.init_app(app)

#データベースモデル定義
class Schedule(db.Model):
    __tablename__='スケジュール'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    date = db.Column(db.DATE)
    starttime = db.Column(db.TIME)
    endtime = db.Column(db.TIME)
    title = db.Column(db.VARCHAR(255))
    content = db.Column(db.TEXT)
    user_id = db.Column(db.INT, db.ForeignKey('ユーザー.id'))

class User(db.Model):
    __tablename__='ユーザー'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    user_name = db.Column(db.VARCHAR(32))
    user_password = db.Column(db.VARCHAR(32))
    
    schedule = db.relationship('Schedule', backref = db.backref('ユーザー'), lazy = True)



#ログイン処理
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userのインスタンスを作成
        user = User(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')