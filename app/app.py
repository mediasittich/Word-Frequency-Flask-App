import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    var = 'Hello from FLASK!'
    return render_template('index.html', var=var)

# TODO: on submit display 'file uploaded successfully' or 'no file selected/invalid file'
# TODO: when file upload success, display filename and a button 'view text analysis'