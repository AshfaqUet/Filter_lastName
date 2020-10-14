from app import app
import os
from flask import render_template, request
from app import functions, models


@app.route('/')  # main/index route of the app
def index():  # index function related to index/main route
    return render_template('index.html', goal=1)


@app.route('/uploads', methods=['GET', 'POST'])  # route at which we uploads the file
def uploads():  # upload folder to upload the file in the app
    uploadfolder = './uploads/'  # Uploading folder where we store the uploaded files
    if request.method == 'POST':  # if form submitted by post method
        try:
            os.mkdir(uploadfolder)

        except:
            pass
        file = request.files['file']  # store the uploaded file in the file variable
        if file:  # if file stored in file variable successfully
            filename = file.filename  # storing filename from file in the variable
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # here is the main point upload the
            # file in the app
            return render_template('index.html', goal=2, filename=filename)  # return the webpage
        else:  # if file not uploaded successfully
            return "File not uploaded successfully"
    return render_template('index.html')


@app.route('/filter/<filename>', methods=['GET', 'POST'])
def filter(filename):
    functions.preprocess_the_name_file(filename)
    last_name = ' Siddique'
    last_name = last_name.upper()
    filter_name, count = functions.filter_names(filename, last_name)
    return render_template('index.html', filtered_names=filter_name, filename=filename, count=count, goal=3)


@app.route('/store', methods=['GET', 'POST'])
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
        if success:
            names = models.File.query.order_by(models.File.id)
    return render_template('index.html', filtered_names=filter_name, names=names, goal=4)
