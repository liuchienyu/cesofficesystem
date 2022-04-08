from flask import Flask, Blueprint, flash, render_template, redirect, url_for, render_template, request, session, g
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import timedelta
from django.contrib.auth.decorators import login_required
import pdfkit
from test_email import sendpaper
from functools import wraps

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Anthony', password='1234'))
users.append(User(id=2, username='Becca', password='secret'))
users.append(User(id=3, username='Carlos', password='somethingsimple'))

app = Flask(__name__)
#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.session_protection = "strong"
#login_manager.login_view = 'login'
#login_manager.login_message = '請證明你並非來自黑暗草泥馬界'
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"
#app.permanent_session_lifetime = timedelta(minutes=5)




"""""
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
"""



@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

def login_required(a):
    @wraps(a)
    def wrap(*args,**kwargs):
        if not g.user:
            return redirect('/login')
        else:
            return a(*args,**kwargs)
            
    return wrap

"""""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login-a.html")

    使用者 = request.form['user_id']
    if (使用者 in users) and (request.form['password'] == users[使用者]['password']):
        user = User()
        user.id = 使用者
        login_user(user)
        return redirect(url_for('home'))

    flash('登入失敗了...')
    return render_template('login-a.html')
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
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
    return render_template("sendnew.html")


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


if __name__ == "__main__":
    app.run(debug=True)
