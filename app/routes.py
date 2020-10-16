from app import app
import os
from flask import request, render_template, jsonify
from app import functions, models


@app.route('/')
def index():
    return ("Hello its index route")


@app.route('/uploads', methods=['POST'])     # route at which we uploads the file
def uploads():                                      # upload folder to upload the file in the app
    uploadfolder = './uploads/'                     # Uploading folder where we store the uploaded files
    if request.method == 'POST':                    # if form submitted by post method
        try:
            os.mkdir(uploadfolder)
        except:
            pass
        file = request.files['file']                # store the uploaded file in the file variable
        if file:                                    # if file stored in file variable successfully
            filename = file.filename                # storing filename from file in the variable
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   filename))       # here is the main point upload the file in the app
            return "File Uploaded Successfully"
        else:                                       # if file not uploaded successfully
            return "File not uploaded successfully"


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
