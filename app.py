from locale import ABDAY_6
from flask import Flask, Blueprint, flash, render_template, redirect, url_for, render_template, request, session, g
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from flask_sqlalchemy import SQLAlchemy
import pdfkit, os
from test_email import sendpaper
from test_data import document_code_data_in
from functools import wraps
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import User
import pymongo
from pymongo import MongoClient
################################


app = Flask(__name__)
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

users=db_session.query(User.username,User.id_name,User.id_sex,User.id_birth,User.id_phone,User.id_email,User.username,User.password).all()


#datebase2
CONNECTION_STRING ="mongodb+srv://dandy40605:1234@cluster0.qqbqe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING,tls=True, tlsAllowInvalidCertificates=True,tz_aware=True )#tls=True, tlsAllowInvalidCertificates=True為解決無法連線問題



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
        print(user1)
        print(user2)
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
    db = client.systemdata
    base_info = db.document_code_data
    count_results = base_info.count_documents({'category':'文號申請'})
    return render_template("home.html", count_results= count_results)


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
        alert_base = '公文送出完成'
        alert_base_herf = 'send_paper'
        return render_template("alert_base.html",alert_base=alert_base,alert_base_herf = alert_base_herf)

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


@app.route("/send_paper_number", methods=['POST'])
@login_required
def send_paper_number():
    if request.method == 'POST':
        a1 = request.values['font']
        a2 = request.values['font']+'第'+request.values['department']+request.values['category']
        a3 = request.values['speed']#+request.values['special']
        a4 = request.values['secretLevel']#+request.values['secret']
        a5 = request.values['appendix']
        a6 = request.values['applicant']
        a7 = request.values['recipient']
        document_code_data_in(a1, a2, a3, a4, a5,a6,a7)
        alert_base = '申請送出完成'
        alert_base_herf = 'paper_number_show'
        return render_template("alert_base.html",alert_base=alert_base,alert_base_herf = alert_base_herf)

@app.route("/papernumber_show")
@login_required
def papernumber_show():
    db = client.systemdata
    base_info = db.document_code_data
    code_results = base_info.find({'category':'文號申請'})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(10)#限制數量
    return render_template("papernumber_show.html",code_results=code_results)


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

@app.route("/testpage")
@login_required
def tastpage():
    return render_template("tastpage.html")


@app.route("/secretary_room_page")
@login_required
def secretary_room_page():
    return render_template("secretary_room_page.html")

@app.route("/finance_department_page")
@login_required
def finance_department_page():
    return render_template("finance_department_page.html")

@app.route("/information_department_page")
@login_required
def information_department_page():
    return render_template("information_department_page.html")

@app.route("/HR_department")
@login_required
def HR_department():
    return render_template("HR_department.html")

if __name__ == "__main__":
    app.run(debug=True)
