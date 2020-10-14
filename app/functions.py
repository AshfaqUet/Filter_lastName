from app import app, models, db
import os
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


def filter_names(filename, last_name):
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
    count = 0
    filtered_names = []  # creating an empty list to append the filtered name in this list as a result
    for i in names:  # Checking each item of the names one by one
        if i.find(last_name) != -1:  # if the item(i) contain name siddique in its full name
            filtered_names.append(i)
            count += 1
    return filtered_names, count


def enter_name_in_database(filtered_names,filename):
    success = True
    existing_names = []
    names = models.File.query.order_by(models.File.id)
    for name in names:
        existing_names.append(name.name)
    for name in filtered_names:
        if name not in existing_names:
            new_name = models.File(name = name,filename = filename)         # creating to do object
        else:
            continue
        try:
            db.session.add(new_name)
            db.session.commit()
        except:
            success = False
    return success