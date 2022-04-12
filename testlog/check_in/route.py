from flask import Blueprint, render_template
from  ..decorators  import login_required

check_in = Blueprint('check_in',__name__)

@check_in.route("/ClockIn")
@login_required
def ClockIn():
    return render_template("ClockIn.html")

@check_in.route("/go_to_work")
@login_required
def go_to_work():
    return render_template("alert_gtw.html")