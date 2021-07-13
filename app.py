import flask
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from Analizer import analize_file
import datetime

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
            return response, 500


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
    objs_list = [[['Age', 'Quantity'], [12, 12], [13, 1], [14, 7], [15, 45], [16, 76]],
                 [['Task', 'Hours per Day'], ['Hombres', 40], ['Mujeres', 50], ['Otro', 10]], ['CDMX', 10], ['JAL', 90]]
    return flask.render_template('base.html', objs_list=objs_list)


@app.route('/add', methods=["POST"])
def add():
    title = flask.request.form.get("title")  # get title from form
    return flask.redirect(flask.url_for("index"))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    # update state of item
    # todo = Todo.query.filter_by(id=todo_id).first()
    # todo.complete = not todo.complete
    # db.session.commit()
    return flask.redirect(flask.url_for("index"))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # delete state of item
    # todo = Todo.query.filter_by(id=todo_id).first()
    # db.session.delete(todo)
    # db.session.commit()
    return flask.redirect(flask.url_for("index"))


if __name__ == "__main__":
    # db.create_all()
    # add something to data base
    app.run(debug=True, host='0.0.0.0')
