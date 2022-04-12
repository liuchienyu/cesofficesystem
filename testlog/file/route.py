import os
from flask import Blueprint, render_template, request
from  ..decorators import login_required
from .test_email import sendpaper
import pdfkit
from werkzeug.utils import secure_filename

file_name = Blueprint('file_name',__name__)
UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


@file_name.route("/download")
@login_required
def download():
    return render_template("download.html")


@file_name.route("/download_to", methods=['POST'])
@login_required
def download_to():
    if request.values['password name'] == '1234':
        html_name = request.values['firstname']
        save_name = request.values['lastname'] + '.pdf'
        pdfkit.from_url(html_name, save_name)
        return render_template("home.html")
    else:
        return render_template("download.html")


@file_name.route("/send")
@login_required
def send():
    return render_template("send.html")


@file_name.route("/send_paper", methods=['POST'])
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

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        
@file_name.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filerename = request.form['filefor']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(file_name.config['UPLOAD_FOLDER'], filename))
            os.chdir(UPLOAD_FOLDER)
            os.rename(filename,  filerename)
            return render_template("uploaded_file.html")
    return render_template("uploaded_file.html")  