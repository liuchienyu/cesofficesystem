from datetime import timedelta
from functools import wraps
import os
from flask import Flask, g, redirect, session
from flask_sqlalchemy import SQLAlchemy
from requests import Session
from sqlalchemy import create_engine
from testlog.__init__ import  User
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

app = Flask(__name__,template_folder='testlog/templates', static_folder="testlog/static",static_url_path="/static")
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"
app.permanent_session_lifetime = timedelta(minutes=30)
UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

db = SQLAlchemy()
#datebase1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BASE_DIR=os.path.dirname(os.path.realpath(__file__))
connection_string = "sqlite:///"+os.path.join(BASE_DIR,'site.db')
engine=create_engine(connection_string,echo=True,connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
db_session = Session()

userss=db_session.query(User.username,User.id_name,User.id_sex,User.id_birth,User.id_phone,User.id_email,User.username,User.password).all()





@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in userss if x[0] == session['user_id']][0]
        g.user = user

def login_required(a):
    @wraps(a)
    def wrap(*args,**kwargs):
        if not g.user:
            return redirect('/login')
        else:
            return a(*args,**kwargs)
            
    return wrap

    
from testlog.main.route import main
from testlog.users.route import users
from testlog.check_in.route import check_in
from testlog.file.route import file_name
from testlog.finance.route import financesys
from testlog.papernumber.route import papernumber

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(check_in)
app.register_blueprint(file_name)
app.register_blueprint(financesys)
app.register_blueprint(papernumber)

if __name__ == '__main__':
    app.run(debug=True)