import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String,Integer,create_engine,Column
from flask import Flask,render_template,redirect,request,url_for,abort,jsonify

app=Flask(__name__)
#datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BASE_DIR=os.path.dirname(os.path.realpath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(BASE_DIR,'site.db')

db = SQLAlchemy(app)

# 模型( model )定義
class User(db.Model):
    #成員編號
    id_number = Column(String(10), unique=True,primary_key=True)
    #姓名
    id_name = Column(String(30), unique=True, nullable=False)
    #性別
    id_sex = Column(String(5), unique=False, nullable=False)
    #生日
    id_birth = Column(String(15), unique=False, nullable=False)
    #聯絡電話
    id_phone = Column(String(10), nullable=False)
    #電子郵件
    id_email = Column(String(100), unique=True, nullable=False)
    #帳號
    username = Column(String(10), unique=True, nullable=False)
    #密碼
    password = Column(String(10), nullable=False)


    def __init__(self, id_number, id_name,  id_sex, id_birth, id_phone, id_email, username, password ):
        self.id_number = id_number
        self.id_name = id_name
        self. id_sex =  id_sex
        self.id_birth = id_birth
        self.id_phone = id_phone
        self. id_email =  id_email
        self.username = username
        self.password = password
"""""
@app.route('/<string:username>/<string:password>',methods=['POST','GET'])
def Insert_User(username,password):
    #判斷資料庫表中是否已經存在了此使用者，如果存在，則不進行插入資料
    data=User.query.filter(User.username==username).all()
    if data==[]:
        # 建立物件，進行資料的插入
        mos = User(username=username, password=password)
        # 建立session
        db.session.add(mos)
        db.session.commit()
        # 關閉資料庫
        db.session.close()
        return jsonify('Add the data Successed!')
    else:
        return jsonify('The data have been existed!')
"""   

@app.route('/index',methods=['POST','GET'])
def index():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        return redirect(url_for('Insert_User',username=username,password=password))
    return render_template('test.html')

@app.route('/research',methods=['POST','GET'])
def research():
    if request.method=='POST':
        researh_id=request.form.get('researh_id')
        researh_in=request.form.get('researh_in')
        return redirect(url_for('return_User',researh_id=researh_id,researh_in=researh_in))
    return render_template('test2.html')

@app.route('/<string:researh_id>/<string:researh_in>',methods=['POST','GET'])
def return_User(researh_id,researh_in):
    m = researh_id
    n = researh_in
    if m=="id_number":
        query = User.query.filter_by(id_number=n).first()
        print(query.id_number)
        return render_template('returntest.html',id_number = query.id_number,id_name=query.id_name)
    else:
        return jsonify('搜尋錯誤!')

if __name__ == '__main__':
    app.run(debug=True)