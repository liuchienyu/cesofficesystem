from flask import Flask, Blueprint, flash, render_template, redirect, url_for, render_template, request, session, g
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from flask_sqlalchemy import SQLAlchemy
import pdfkit, os
from test_email import sendpaper
from functools import wraps
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import User



app = Flask(__name__)
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"
app.permanent_session_lifetime = timedelta(minutes=5)
UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

db = SQLAlchemy()
#datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BASE_DIR=os.path.dirname(os.path.realpath(__file__))
connection_string = "sqlite:///"+os.path.join(BASE_DIR,'site.db')
engine=create_engine(connection_string,echo=True,connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
db_session = Session()

users=db_session.query(User.username,User.id_name,User.id_sex,User.id_birth,User.id_phone,User.id_email,User.username,User.password).all()


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x[0] == session['user_id']][0]
        g.user = user

def login_required(a):
    @wraps(a)
    def wrap(*args,**kwargs):
        if not g.user:
            return redirect('/login')
        else:
            return a(*args,**kwargs)
            
    return wrap

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username_r = request.form['username']
        password_r = request.form['password']
        
        user1 = db_session.query(User.username).filter(User.username == username_r).first()
        user2 = db_session.query(User.password).filter(User.password == password_r ).first()
        if  user1 != None and user2 != None :
            session['user_id'] = username_r
            return redirect(url_for('home'))

        return redirect(url_for('login'))

    return render_template('login-a.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/")
@login_required
def homepage():
    return render_template("home.html")

@app.route("/home")
@login_required
def home():
    return render_template("home.html")


@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html')

@app.route("/more")
@login_required
def more():
    return render_template("more_profile.html")


@app.route("/download")
@login_required
def download():
    return render_template("download.html")


@app.route("/download_to", methods=['POST'])
@login_required
def download_to():
    if request.values['password name'] == '1234':
        html_name = request.values['firstname']
        save_name = request.values['lastname'] + '.pdf'
        pdfkit.from_url(html_name, save_name)
        return render_template("home.html")
    else:
        return render_template("download.html")


@app.route("/send")
@login_required
def send():
    return render_template("send.html")


@app.route("/send_paper", methods=['POST'])
@login_required
def send_paper():
    if request.values['password name'] == '1234':
        a1 = request.values['userfor']
        a2 = request.values['time_y']
        a3 = request.values['time_m']
        a4 = request.values['time_d']
        a5 = request.values['letter_1']
        sendpaper(a1, a2, a3, a4, a5)
        send_alert = '發送完成' 
        return render_template("alert_paper.html")

    else:
        return render_template("send.html")


@app.route("/ClockIn")
@login_required
def ClockIn():
    return render_template("ClockIn.html")

@app.route("/go_to_work")
@login_required
def go_to_work():
    return render_template("alert_gtw.html")


@app.route("/finance")
@login_required
def finance():
    return render_template("finance.html")


@app.route("/Leave")
@login_required
def Leave():
    return render_template("Leave.html")


@app.route("/overtime")
@login_required
def overtime():
    return render_template("overtime.html")

@app.route("/profile_setting",methods=['GET', 'POST'])
@login_required
def profile_setting():
    return render_template("profile_setting_base.html")

@app.route("/profile_updata", methods=['GET', 'POST'])
@login_required
def profile_updata():
    if request.method == 'POST':
        newin = request.form['new_id_name']
        res = db_session.query(User).filter_by(id_name=g.user.id_name).update({'id_name':newin})
        db_session.commit()
        db_session.close()
        return redirect(url_for('more'))

@app.route("/paper_number")
@login_required
def paper_number():
    return render_template("paper_number.html")








def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filerename = request.form['filefor']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.chdir(UPLOAD_FOLDER)
            os.rename(filename,  filerename)
            return render_template("uploaded_file.html")
    return render_template("uploaded_file.html")  



if __name__ == "__main__":
    app.run(debug=True)
