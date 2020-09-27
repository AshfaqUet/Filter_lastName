from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)           # initializing flask app
UPLOAD_FOLDER = './uploads/'     # Uploading folder where we store the uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER     # config the folder name

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filter_name.db'
db = SQLAlchemy(app)

class add_name(db.Model):           # data base table class used for adding the filtered names in db (Task 1 Goal No 4)
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(200),nullable = False)
    filename = db.Column(db.String(200),nullable = False)

@app.route('/')                 # main/index route of the app
def index():                    # index function related to index/main route
    return render_template('index.html', goal = 1)



@app.route('/uploads', methods =['GET','POST'] )    # route at which we uploads the file
def uploads():                                      # upload folder to upload the file in the app
    if request.method == 'POST':            # if form submitted by post method
        try:
            os.mkdir(UPLOAD_FOLDER)
        except:
            pass
        file = request.files['file']        # store the uploaded file in the file variable
        if file:                # if file stord in file variable successfully
            filename = file.filename        # storing filename from file in the variable
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))      # here is the main point upload the
                                                                                # file in the app
            return render_template('index.html', goal = 2,filename = filename)        # return the webpage
        else:           # if file not uploaded successfully
            return "File not uploaded successfully"
    return render_template('index.html')

################################### Funciton related to task 1 goal no 2 and 3 #################################################
def preprocess_the_name_file(filename):
    """
    It is a funciton which preprocess the file before filtering the person having last name = siddique
    1. open a file and remove , character from the file because we consider a file where names are seperated by ,
    2. CAPATALIZE all the character of the file file so that searching should be easy
    :param filename: filename is required on which you want to apply the preprocess method
    :return: None
    """
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(path, "rt") as file:
        content = file.read()
    content = content.replace(',', '\n')
    content = content.upper()
    with open(path, 'w') as file:
        file.write(content)


def filter_names(filename,last_name):
    """
    This function filter out the person in file = filename having last name = last_name
    :param filename: filename is required from which we filter out the person having last name
    :param last_name: Last name on which you want to filter out the users
    :return: return a list of filterd persons who have last name = parameteric lastname
    :return: it also return the count of people having last name = parametric lastname
    """
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(path, "rt") as file:
        names = file.readlines()
    last_name = last_name
    count_last_name = 0
    filtered_names = []  # creating an empty list to append the filtered name in this list as a result
    for i in names:  # Checking each item of the names one by one
        if i.find(last_name)!= -1:  # if the item(i) contain name siddique in its full name
            filtered_names.append(i)
            count_last_name +=1
    return filtered_names,count_last_name

 ##################################### Route of Goal No 2 and 3 #######################################

@app.route('/filter/<filename>', methods = ['GET','POST'])
def filter(filename):
    path = "./uploads"
    directories = os.listdir(path)
    filter_name = []
    preprocess_the_name_file(filename)
    last_name = ' Siddique'
    last_name = last_name.upper()
    filter_name,count = filter_names(filename,last_name)
    return render_template('index.html', filtered_names=filter_name,filename = filename, count=count,goal = 3)

####################################### Function related to task 1 Goal No 4 #################################
def enter_name_in_database(filtered_names,filename):
    success = True
    existing_names = []
    names = add_name.query.order_by(add_name.id)
    for name in names:
        existing_names.append(name.name)
    for name in filtered_names:
        if name not in existing_names:
            new_name = add_name(name = name,filename = filename)         # creating to do object
        else:
            continue
        try:
            db.session.add(new_name)
            db.session.commit()
        except:
            success = False
    return success

###################################### Route of Goal No 4 ######################################################
@app.route('/store_name', methods = ['GET','POST'])
def store_name():
    path = "./uploads"
    directories = os.listdir(path)
    filter_name = []
    for filename in directories:
        preprocess_the_name_file(filename)
        last_name = ' SIDDIQUE'
        filtered_names,count = filter_names(filename,last_name)
        filter_name = filter_name + filtered_names
        success = enter_name_in_database(filtered_names,filename)
        if success:
            names = add_name.query.order_by(add_name.id)
    return render_template('index.html',filtered_names = filter_name, names = names,goal = 4)



if __name__ == "__main__":
    app.run(debug=True)
