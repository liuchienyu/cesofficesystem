import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String,Integer,create_engine,Column
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()
#datebase1
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

BASE_DIR=os.path.dirname(os.path.realpath(__file__))
connection_string = "sqlite:///"+os.path.join(BASE_DIR,'site.db')
engine=create_engine(connection_string,echo=True,connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
db_session = Session()

users=db_session.query(User.username,User.id_name,User.id_sex,User.id_birth,User.id_phone,User.id_email,User.username,User.password).all()
