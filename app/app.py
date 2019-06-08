import os
import nltk
import pandas as pd
import plotly
import plotly.graph_objs as go
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'dev'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_plot(x_list,y_list):
    data = [
        go.Bar(
            x=x_list,
            y=y_list
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        # confirm that POST request has the correct field name set
        if 'fileToUpload' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['fileToUpload']

        # check if file was selected by user
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        # check if file extension is valid
        if not allowed_file(file.filename):
            flash('Only .txt files allowed. Please select another file.')
            return redirect(request.url)
        
        # check if file exists and has a valid extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully!')
            return redirect(request.url)

    print(os.listdir(UPLOAD_FOLDER))
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('upload.html', files=files)

@app.route('/<file>')
def show_stats(file):
    # load text
    f = open(UPLOAD_FOLDER + '/' + file + '.txt', 'r')
    raw = f.read()

    # text processing
    tokenizer = nltk.tokenize.RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(raw)

    words = []

    for word in tokens:
        words.append(word.lower())
    
    sw = nltk.corpus.stopwords.words('english')
    
    words_ns = []

    for word in words:
        if word not in sw:
            words_ns.append(word)
    
    freqdist = nltk.FreqDist(words_ns)
    freqdist.most_common(25)

    df_fdist = pd.DataFrame.from_dict(freqdist, orient='index')
    df_fdist = df_fdist.reset_index()
    df_fdist.columns = ['Word', 'Frequency']
    df_fdist = df_fdist.sort_values(by='Frequency', ascending=False)

    bar = create_plot(df_fdist['Word'][:25], df_fdist['Frequency'][:25])

    return render_template('textspecs.html',file=file, sorted_words=freqdist.most_common(25), plot=bar)

# TODO: on submit display 'file uploaded successfully' or 'no file selected/invalid file'
# TODO: when file upload success, display filename and a button 'view text analysis'
