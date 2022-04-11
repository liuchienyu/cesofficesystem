import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename



app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filerename = request.form['filefor']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.chdir(UPLOAD_FOLDER)
            os.rename(filename,  filerename)
            return render_template("uploaded_file.html")
    return render_template("uploaded_file.html") 



'''
from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
'''
if __name__ == '__main__':
    app.run(debug=True)