from functools import wraps
import os
from flask import Blueprint, g, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from ..models import *
from ..__init__ import Session, db_session, User
from  ..decorators  import login_required
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

users = Blueprint('users',__name__)
db = SQLAlchemy()
BASE_DIR=os.path.dirname(os.path.realpath(__file__))
connection_string = "sqlite:///"+os.path.join(BASE_DIR,'site.db')
engine=create_engine(connection_string,echo=True,connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)


db_session = Session()

users_data=db_session.query(User.username,User.id_name,User.id_sex,User.id_birth,User.id_phone,User.id_email,User.username,User.password).all()



@users.route('/login', methods=['GET', 'POST'])
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
            print(session['user_id'])
            return redirect(url_for('main.home'))

        return redirect(url_for('users.login'))

    return render_template('login-a.html')

@users.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('users.login'))

@users.route("/profile")
@login_required
def profile():
    return render_template('profile.html')

@users.route("/more")
@login_required
def more():
    return render_template("more_profile.html")

@users.route("/profile_setting",methods=['GET', 'POST'])
@login_required
def profile_setting():
    return render_template("profile_setting_base.html")

@users.route("/profile_updata", methods=['GET', 'POST'])
@login_required
def profile_updata():
    if request.method == 'POST':
        newin = request.form['new_id_name']
        res = db_session.query(User).filter_by(id_name=g.user.id_name).update({'id_name':newin})
        db_session.commit()
        db_session.close()
        return redirect(url_for('more'))