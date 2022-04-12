from flask import Blueprint, render_template
from  ..decorators  import login_required

main = Blueprint('main',__name__)



@main.route("/")
@login_required
def homepage():
    return render_template("home.html")

@main.route("/home")
@login_required
def home():
    return render_template("home.html")

@main.route("/testpage")
@login_required
def tastpage():
    return render_template("tastpage.html")

@main.route("/Leave")
@login_required
def Leave():
    return render_template("Leave.html")


@main.route("/overtime")
@login_required
def overtime():
    return render_template("overtime.html")