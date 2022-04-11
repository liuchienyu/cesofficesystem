import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import Column, String, Integer

app = Flask(__name__)

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
    id_sex = Column(String(50), unique=False, nullable=False)
    #生日
    id_birth = Column(String(150), unique=False, nullable=False)
    #聯絡電話
    id_phone = Column(String(100), nullable=False)
    #電子郵件
    id_email = Column(String(100), unique=True, nullable=False)
    #帳號
    username = Column(String(100), unique=True, nullable=False)
    #密碼
    password = Column(String(100), nullable=False)


    def __init__(self, id_number, id_name,  id_sex, id_birth, id_phone, id_email, username, password ):
        self.id_number = id_number
        self.id_name = id_name
        self. id_sex =  id_sex
        self.id_birth = id_birth
        self.id_phone = id_phone
        self. id_email =  id_email
        self.username = username
        self.password = password


@app.route('/')
def index():
    #Create data
    db.create_all()

    return 'ok'


@app.route('/add')
def add():
    new_user=User(
        id_number = input('請輸入識別證號'),
        id_name = input('請輸入姓名'),
        id_sex = input('請輸入性別'),
        id_birth = input('請輸入生日'),
        id_phone = input('請輸入電話'),
        id_email = input('請輸入信箱'),
        username = input('請輸入使用者名稱'),
        password =(input('請輸入密碼')))

    db.session.add(new_user)

    db.session.commit()
    print("建立完成")
    print(new_user)
    return "建立完成"
# Add data
#product_max = Product('Max', 8888,'https://picsum.photos/id/1047/1200/600', '', '')
#db.session.add(product_max)
#db.session.commit()

# Read data
@app.route('/read')
def read():
    m = input('請輸入搜尋目標')
    n = input('請輸入搜尋目標內容')
    query = User.query.filter_by(m=n).first()
    print(query.id_name)
    return str(query.id_name)

# Delete data
#query = Product.query.filter_by(name='Max').first()
#db.session.delete(query)
#db.session.commit()

# Updata data
# query = Product.query.filter_by(name='Max').first()

# 將 price 修改成 10 塊
#query.price = 10
#db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)