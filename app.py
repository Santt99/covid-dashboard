import flask
from flask import Flask, request, jsonify, redirect
from werkzeug.utils import redirect, secure_filename
import os
from Analizer import analize_file
import datetime
import json

app = flask.Flask(__name__)

RESULT_FOLDER = "./results"
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            analize_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/", code=302)



# index
@app.route('/')
def index():
    # show todos
    '''
    [
        ['Genre', 'Fantasy & Sci Fi', 'Romance', 'Mystery/Crime', 'General',
         'Western', 'Literature', { role: 'annotation' } ],
        ['2010', 10, 24, 20, 32, 18, 5, ''],
        ['2020', 16, 22, 23, 30, 16, 9, ''],
        ['2030', 28, 19, 29, 30, 12, 13, '']
      ]
    '''
    bys = ["SEXO", "ENTIDAD_RES", "TIPO_PACIENTE", "EDAD"]
    analizor = analize_file()
    objs_list = {}
    if type(analizor) != type(None) :
        valid_columns = analizor.columns
        if set(bys).issubset(set(valid_columns)):
            for by in bys:
                objs_list[by] = analizor[by].value_counts().to_json()
                print(objs_list[by])
            
    return flask.render_template('base.html', objs_list=objs_list)

    
    


if __name__ == "__main__":
    # db.create_all()
    # add something to data base
    app.run(debug=True, host='0.0.0.0')
