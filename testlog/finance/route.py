from flask import Blueprint, render_template
from  testlog.decorators  import login_required
financesys = Blueprint('financesys',__name__)


@financesys.route("/finance")
@login_required
def finance():
    return render_template("finance.html")