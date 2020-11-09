from app import app
import os
from flask import request, jsonify
from app import functions, models
from werkzeug.utils import secure_filename

# ######################################### INDEX ###########################################################


@app.route('/')
def index():
    return "Hello its index route"


# ########################################### UPLOADS ########################################################
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads', methods=['POST'])
def uploads():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

# ################################################ FILTER ##################################################


@app.route('/filter/<string:filename>', methods=['GET'])
def filter(filename):
    path = "./uploads"
    directories = os.listdir(path)
    if filename in directories:
        functions.preprocess_the_name_file(filename)
        last_name = ' Siddique'
        last_name = last_name.upper()
        filter_name, count = functions.filter_names(filename, last_name)
        result = {
            "filter_name": filter_name,
            "count": count
        }
        return jsonify(result)
    else:
        return "File not exist in database"

# ############################################## STORE #####################################################


@app.route('/store', methods=['GET'])
def store():
    path = "./uploads"
    directories = os.listdir(path)
    filter_name = []
    for filename in directories:
        functions.preprocess_the_name_file(filename)
        last_name = ' SIDDIQUE'
        filtered_names, count = functions.filter_names(filename, last_name)
        filter_name = filter_name + filtered_names
        success = functions.enter_name_in_database(filtered_names, filename)

    names_list = [item.name for item in models.File.query.all()]
    print(names_list)
    result = {
        'names': names_list
    }
    return jsonify(result)
