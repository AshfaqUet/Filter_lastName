import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'you-will-never-guess'  # this is used for encryption purpose mostly app
                                                # use this for encryption with the secret_key of env variable
                                                # and if no env is defined then use second string
    UPLOAD_FOLDER = './uploads'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'username'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'filter')
)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
