from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from Analizer import analize_file
import datetime

RESULT_FOLDER = "./results"
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

if not os.path.exists(RESULT_FOLDER):
    os.mkdir(RESULT_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "The file you try to upload dosen't have a name", 500
        file = request.files['file']
        if file.filename == '':
            return "The file you try to upload dosen't have a name", 500
        if file and allowed_file(file.filename):
            
            filename = "{}-".format(datetime.datetime.now()) + secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            analize_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "File {} was saved successfully".format(filename), 200


@app.route("/analize", methods=["GET"])
def analize():
    if request.method == 'GET':
        body = request.get_json()
        file_name = body["file-name"]
        by = list(body["by"])
        analizor = analize_file(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        valid_columns = analizor.columns
        if set(by).issubset(set(valid_columns)):
            result = analizor[by]
            result_json = result.to_json()
            response = jsonify(result_json)
            return response
        else:
            response = "One fo this keys is not a valid column {}, please use one of this: {}".format(by, valid_columns)
            print(response)
            return response , 500