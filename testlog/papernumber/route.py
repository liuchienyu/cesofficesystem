from flask import Blueprint, render_template
from werkzeug import Client
import pymongo
from pymongo import MongoClient
from  testlog.decorators  import login_required

papernumber = Blueprint('papernumber',__name__)




@papernumber.route("/paper_number")
@login_required
def paper_number():
    return render_template("paper_number.html")

@papernumber.route("/papernumber_show")
@login_required
def papernumber_show():
    #datebase2
    CONNECTION_STRING ="mongodb+srv://dandy40605:1234@cluster0.qqbqe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING,tls=True, tlsAllowInvalidCertificates=True,tz_aware=True )#tls=True, tlsAllowInvalidCertificates=True為解決無法連線問題

    db = client.systemdata
    base_info = db.document_code_data
    code_results = base_info.find({'category':'文號申請'})
    code_results.sort("make_time",pymongo.DESCENDING)#按照時間降序排列
    code_results.limit(10)#限制數量
    return render_template("papernumber_show.html",code_results=code_results)