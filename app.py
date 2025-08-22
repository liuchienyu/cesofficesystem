import datetime
import time
from flask import Flask, render_template, redirect, url_for, render_template, request, session, g
from flask_login import  login_required
from datetime import timedelta,date
from django.contrib.auth.decorators import login_required
from flask_sqlalchemy import SQLAlchemy
import pdfkit, os
from test_email import sendpaper
from data_input import announcement_imput, clockin, document_code_data_in, law_system_imput
from functools import wraps
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import User
import pymongo
from pymongo import MongoClient
from finance import money_m,finance_imput
from flask import jsonify, send_from_directory
from bson.objectid import ObjectId
################################


app = Flask(__name__)
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"
app.permanent_session_lifetime = timedelta(hours=2)
UPLOAD_FOLDER = './static/download_file'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
# 設定為 +8 時區
tz = datetime.timezone(datetime.timedelta(hours=+8))

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
CONNECTION_STRING ="mongodb+srv://dandy40605:dandy1234@cluster0.qqbqe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
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
            return render_template('./login/login_wait.html')

        return redirect(url_for('login'))

    return render_template('./login/login-a.html')



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
    base_info2 = db.announcement
    base_info3 = db.law_system
    base_info4 = db.base_info
    count_results = base_info.count_documents({'category':'文號申請'})
    count_results2 = base_info2.count_documents({'category':'公告'})
    count_results3 = base_info3.count_documents({'category':'法務案件'})
    code_results = base_info.find({'category':'文號申請'})
    code_results2 = base_info2.find({'category':'公告'})
    code_results3 = base_info2.find({'announcement_category':'財務公告'})
    code_results4 = base_info2.find({'announcement_category':'人資公告'})
    code_results5 = base_info3.find({'category':'法務案件'})

    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results2.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results3.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results4.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results5.sort("make_time",pymongo.DESCENDING)#按照時間降序排列


    code_results.limit(5)#限制數量
    code_results2.limit(5)#限制數量
    code_results3.limit(5)#限制數量
    code_results4.limit(5)#限制數量
    code_results5.limit(5)#限制數量

    time_money = format(int(money_m(session['user_id'])),',')

    return render_template("home.html", 
    count_results= count_results,
    count_results2= count_results2,
    count_results3= count_results3,
    code_results = code_results,
    code_results2 = code_results2,
    code_results3 = code_results3,
    code_results4 = code_results4,
    code_results5 = code_results5,
    time_money = time_money)

@app.route("/activity_record")
@login_required
def activity_record():
    db = client.systemdata
    base_info = db.clockin
    count_results = base_info.count_documents({'category':'打卡'})
    code_results = base_info.find({'code_number':session['user_id']})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(10)#限制數量

    return render_template("./profile/activity_record.html",count_results= count_results,code_results = code_results)


@app.route("/profile")
@login_required
def profile():
    db = client.systemdata
    base_info = db.base_info
    count_results = base_info.find({'id_number':session['user_id']})
    results1 = base_info.find_one({'id_number':session['user_id']},{'job_time':1})
    if 'job_time' in results1:
        arr = results1['job_time'].split('-')
        y1=int(arr[0])
        y2=int(arr[1])
        y3=int(arr[2])
        then = date(y1, y2, y3)
        now = date.today()
        count_results2 = str((now - then).days*8) +'小時'
    return render_template('./profile/profile.html',count_results= count_results,count_results2= count_results2)

@app.route("/more")
@login_required
def more():
    db = client.systemdata
    base_info = db.base_info
    count_results = base_info.find({'id_number':session['user_id']})
    results1 = base_info.find_one({'id_number':session['user_id']},{'job_time':1})
    if 'job_time' in results1:
        arr = results1['job_time'].split('-')
        y1=int(arr[0])
        y2=int(arr[1])
        y3=int(arr[2])
        then = date(y1, y2, y3)
        now = date.today()
        count_results2 = str((now - then).days*8) +'小時'
    return render_template("./profile/more_profile.html",count_results= count_results,count_results2= count_results2)


@app.route("/download")
@login_required
def download():
    return render_template("./secretary_room/download.html")


@app.route("/download_to", methods=['POST'])
@login_required
def download_to():
    if request.values['password name'] == '1234':
        html_name = request.values['firstname']
        save_name = request.values['lastname'] + '.pdf'
        pdfkit.from_url(html_name, save_name)
        return render_template("home.html")
    else:
        return render_template("./secretary_room/download.html")


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
        alert_base_herf = 'send'
        return render_template("./base/alert_base.html",alert_base=alert_base,alert_base_herf = alert_base_herf)

    else:
        return render_template("./secretary_room/send.html")


@app.route("/ClockIn")
@login_required
def ClockIn():
    time_1 = datetime.datetime.now(tz).strftime("%H:%M:%S")
    print(time_1)
    if '24:00:00' >=time_1 >= '20:00:00':
        time_base = '現在是上班時間，請記得打上班卡'
        if '21:45:00'>= time_1 >= '20:00:00':
            time_base2= '值班主管、早班成員'
            return render_template("./HR_department/ClockIn.html",time_base=time_base,time_base2=time_base2)
        else:
            time_base2= '值班主管、晚班成員'
            return render_template("./HR_department/ClockIn.html",time_base=time_base,time_base2=time_base2)
    else:
        time_base = '現在是下班時間，請記得打下班卡'
        time_base2 = '無'
        return render_template("./HR_department/ClockIn.html",time_base=time_base,time_base2=time_base2)

@app.route("/go_to_work")
@login_required
def go_to_work():
    a1 = '上班'
    a2 = session['user_id']
    clockin(a1, a2)
    alert_base = '上班打卡完成'
    alert_base_herf = 'ClockIn'
    return render_template("./base/alert_base.html",alert_base=alert_base,alert_base_herf = alert_base_herf)

@app.route("/out_to_work")
@login_required
def out_to_work():
    a1 = '下班'
    a2 = session['user_id']
    clockin(a1, a2)
    alert_base = '下班打卡完成'
    alert_base_herf = 'ClockIn'
    return render_template("./base/alert_base.html",alert_base=alert_base,alert_base_herf = alert_base_herf)

@app.route("/finance_show")
@login_required
def finance_show():
    return render_template("./finance_department/finance_show.html")

@app.route("/finance_in")
@login_required
def finance_in():
    return render_template("./finance_department/finance_in.html")

@app.route("/finance_check")
@login_required
def finance_check():
    return render_template("./finance_department/finance_check.html")


@app.route("/finance_records", methods=["POST",'GET'])
@login_required
def finance_records_page():
    return render_template("./finance_department/Write-off-input.html")
def finance_records_create():
    #接收表單欄位：
    #- project_name (str)
    #- category (str)
    #- amount (number)
    #- payment_method (str)
    #- remark (str, optional)
    #- receipt (file, optional)
    #儲存到 MongoDB：systemdata.finance_reimbursements
    dbm = client.systemdata
    col = dbm.finance_reimbursements

    project_name = request.form.get("project_name", "").strip()
    category = request.form.get("category", "").strip()
    amount_raw = request.form.get("amount", "0").strip()
    payment_method = request.form.get("payment_method", "").strip()
    remark = request.form.get("remark", "").strip()

    # 基本驗證
    if not project_name or not category or not amount_raw or not payment_method:
        return jsonify({"error": "缺少必要欄位"}), 400

    # 金額轉 float
    try:
        amount = float(amount_raw)
    except ValueError:
        return jsonify({"error": "金額格式錯誤"}), 400

    # 處理上傳檔案（可選）
    file_path = None
    if "receipt" in request.files:
        f = request.files["receipt"]
        if f and f.filename:
            filename = secure_filename(f.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            f.save(save_path)
            # 儲存相對路徑，方便前端引用
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    doc = {
        "category": "財務核銷",             # 方便你後台分類
        "project_name": project_name,
        "category_name": category,          # 避免和上面 category 混淆，也存一份細項名稱
        "amount": amount,
        "payment_method": payment_method,
        "receipt_file": file_path,
        "remark": remark,
        "operator": session.get("user_id"), # 紀錄誰送的
        "created_at": datetime.datetime.now(tz).isoformat(),
    }

    result = col.insert_one(doc)
    return jsonify({"message": "Record created", "id": str(result.inserted_id)}), 201

def finance_records_list():
    #回傳最新核銷紀錄，供前端表格渲染
    dbm = client.systemdata
    col = dbm.finance_reimbursements

    # 依時間排序，最新在前
    cursor = col.find({}).sort("created_at", pymongo.DESCENDING)
    records = []
    for r in cursor:
        records.append({
            "id": r.get("id"),
            "project_name": r.get("project_name"),
            "category": r.get("category_name"),         # 前端表格的 category
            "amount": r.get("amount"),
            "payment_method": r.get("payment_method"),
            "remark": r.get("remark"),
            "created_at": r.get("created_at"),
            "receipt_file": r.get("receipt_file"),
            "operator": r.get("operator"),
        })
    return jsonify(records), 200

@app.route("/Leave")
@login_required
def Leave():
    return render_template("./HR_department/leave_form.html")


@app.route("/overtime")
@login_required
def overtime():
    return render_template("./HR_department/overtime.html")

@app.route("/profile_setting",methods=['GET', 'POST'])
@login_required
def profile_setting():
    return render_template("./profile/profile_setting_base.html")

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
    return render_template("./paper/paper_number.html")


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
        alert_base_herf = 'papernumber_show'
        return render_template("./base/alert_base.html",alert_base=alert_base,alert_base_herf = alert_base_herf)

@app.route("/papernumber_show")
@login_required
def papernumber_show():
    db = client.systemdata
    base_info = db.document_code_data
    code_results = base_info.find({'category':'文號申請'})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(10)#限制數量
    return render_template("./paper/papernumber_show.html",code_results=code_results)


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
            return render_template("./secretary_room/uploaded_file.html")
    return render_template("./secretary_room/uploaded_file.html")  

@app.route("/testpage")
@login_required
def tastpage():
    return render_template("tastpage.html")


@app.route("/secretary_room_page")
@login_required
def secretary_room_page():
    return render_template("./secretary_room/secretary_room_page.html")

@app.route("/finance_department_page")
@login_required
def finance_department_page():
    return render_template("./finance_department/finance_department_page.html")

@app.route("/information_department_page")
@login_required
def information_department_page():
    return render_template("./information_department/information_department_page.html")

@app.route("/HR_department")
@login_required
def HR_department():
    return render_template("./HR_department/HR_department.html")

@app.route("/general_management_office")
@login_required
def general_management_office():
    return render_template("./general_management_office/general_management_office.html")

@app.route("/class_schedule")
@login_required
def class_schedule():
    db = client.systemdata
    base_info = db.base_info
    code_results = base_info.find({'category':'個資'})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    return render_template("./HR_department/class_schedule.html",code_results = code_results)

@app.route("/announcement")
@login_required
def announcement():
    db = client.systemdata
    base_info = db.announcement
    code_results = base_info.find({'category':'公告'})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(10)#限制數量
    return render_template("./announcement/announcement.html",code_results=code_results)

#布告欄-每個
@app.route('/announcement/<search_id>')
@login_required
def announcement2(search_id):
    db = client.systemdata
    base_info = db.announcement
    code_results = base_info.find({'search_id':search_id})
    return render_template('./announcement/announcement_each.html',code_results=code_results)

@app.route("/announcement_in", methods=['GET', 'POST'])
@login_required
def announcement_in():
    if request.method == 'POST':
        a1 = request.values['department']  
        a2 = request.values['applicant']
        a3=  request.form['subject']
        a4= request.form['text_in']
        a5 = request.values['announcement_category']
        a6 = request.values['filename']
        announcement_imput(a1, a2,a3,a4,a5,a6)
        alert_base = '公告發布完成'
        alert_base2 = '點此上傳公告附件'
        alert_base_herf = 'announcement'
        alert_base_herf2 = 'upload'
        return render_template("./base/alert_base.html",alert_base=alert_base,alert_base2=alert_base2,alert_base_herf = alert_base_herf,alert_base_herf2=alert_base_herf2)
    return render_template("./announcement/announcement_in.html")  

@app.route("/team_law")
@login_required
def team_law():
    db = client.systemdata
    base_info = db.team_law
    code_results = base_info.find({'category':'法令解釋'})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(10)#限制數量
    return render_template("./general_management_office/team_law.html",code_results=code_results)
#法令解釋-每個
@app.route('/team_law/<search_id>')
@login_required
def team_law2(search_id):
    if search_id == 'L1':
        return render_template('./general_management_office/lawpaper/L1.html')
    elif search_id == 'O1':
        return render_template('./general_management_office/lawpaper/O1.html')
    elif search_id == 'O2':
        return render_template('./general_management_office/lawpaper/O2.html')
        
@app.route("/sign_off")
@login_required
def sign_off():
    return render_template("./secretary_room/sign_off.html")

@app.route("/meeting_minutes")
@login_required
def meeting_minutes():
    db = client.systemdata
    base_info = db.meeting_minutes
    code_results = base_info.find({'category':'會議記錄'})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(10)#限制數量
    return render_template("./secretary_room/meeting_minutes.html",code_results=code_results)
#會議記錄-每個
@app.route('/meeting_minutes/<search_id>')
@login_required
def meeting_minutes2(search_id):
        db = client.systemdata
        base_info = db.team_law
        code_results = base_info.find({'search_id':search_id})
        return render_template('./secretary_room/meeting_minutes_each.html',code_results=code_results)

@app.route("/law_system")
@login_required
def law_system():
    db = client.systemdata
    base_info = db.law_system
    code_results = base_info.find({'category':'法務案件'})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(10)#限制數量
    return render_template("./general_management_office/law_system/law_system.html",code_results=code_results)

@app.route("/progress")
@login_required
def progress():
    db = client.systemdata
    base_info = db.announcement
    code_results = base_info.find({'category':'公告'})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(10)#限制數量
    return render_template("./general_management_office/law_system/progress.html",code_results=code_results)

@app.route("/law_system_in", methods=['GET', 'POST'])
@login_required
def law_system_in():
    if request.method == 'POST':
        a1 = request.values['department']  
        a2 = request.values['applicant']
        a3 =  request.form['subject']
        a4 = request.form['text_in']
        a5 = request.values['law_system_category']
        a6 = request.values['filename']
        a7 = request.values['law_system_category2']
        law_system_imput(a1, a2,a3,a4,a5,a6,a7)
        alert_base = '案件新增完成'
        alert_base2 = '點此上傳案件附件'
        alert_base_herf = 'law_system'
        alert_base_herf2 = 'upload'
        return render_template("./base/alert_base.html",alert_base=alert_base,alert_base2=alert_base2,alert_base_herf = alert_base_herf,alert_base_herf2=alert_base_herf2)
    return render_template("./general_management_office/law_system/law_system_in.html")

@app.route('/law_system/<search_id>')
@login_required
def law_system2(search_id):
    db = client.systemdata
    base_info = db.law_system
    code_results = base_info.find({'search_id':search_id})
    return render_template('./general_management_office/law_system/law_system_each.html',code_results=code_results)

@app.route("/finance_person")
@login_required
def finance_person():
    time_money = money_m(session['user_id'])
    db = client.systemdata
    base_info = db.finance
    code_results = base_info.find({'id_number':session['user_id']})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(10)#限制數量
    return render_template("./test1.html",code_results=code_results,time_money=time_money)

@app.route("/finance_person_in", methods=['GET', 'POST'])
@login_required
def finance_person_in():
    if request.method == 'POST':
        a = request.values['id_number']  
        b = request.values['Salary']
        c = request.form['food_allowance']
        d = request.form['PA_bonus']
        e = request.form['performance_bonus']
        f = request.form['job_added']
        g = request.form['labor_protection']
        h = request.form['health_insurance']
        finance_imput(a,b,c,d,e,f,g,h)
        alert_base = '薪水發放完成'
        alert_base2 = '點此上傳案件附件'
        alert_base_herf = 'finance_person'
        alert_base_herf2 = 'upload'
        return render_template("./base/alert_base.html",alert_base=alert_base,alert_base2=alert_base2,alert_base_herf = alert_base_herf,alert_base_herf2=alert_base_herf2)
    return render_template("./test1_in.html")




if __name__ == "__main__":
    app.run(debug=True)
