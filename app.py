from flask import Flask,Blueprint, flash,render_template, redirect, url_for, render_template,request, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import timedelta
from django.contrib.auth.decorators import login_required
import pdfkit


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請證明你並非來自黑暗草泥馬界'
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"
app.permanent_session_lifetime = timedelta(minutes=5)


class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(使用者):
    if 使用者 not in users:
        return

    user = User()
    user.id = 使用者
    return user

@login_manager.request_loader
def request_loader(request):
    使用者 = request.form.get('user_id')
    if 使用者 not in users:
        return

    user = User()
    user.id = 使用者

    user.is_authenticated = request.form['password'] == users[使用者]['password']

    return user

users = {'Me': {'password': 'myself'}}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login-a.html")
    
    使用者 = request.form['user_id']
    if (使用者 in users) and (request.form['password'] == users[使用者]['password']):
        user = User()
        user.id = 使用者
        login_user(user)
        flash(f'{使用者}！歡迎加入草泥馬訓練家的行列！')
        return redirect(url_for('home'))

    flash('登入失敗了...')
    return render_template('login-a.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route("/")
def homepage():
    return redirect(url_for('login'))

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/profile")
def profile():
    return render_template("./profile.html")

@app.route("/more")
def more():
    return render_template("more_profile.html")

@app.route("/download")
def download():
    return render_template("download.html")

@app.route("/download_to", methods=['POST'])
def download_to():
    if request.values['password name'] == '1234':
        html_name = request.values['firstname']
        save_name = request.values['lastname'] +'.pdf'
        pdfkit.from_url(html_name,save_name)
        return render_template("home.html")
    else:
        return render_template("download.html")



if __name__ == "__main__":
    app.run(debug=True)