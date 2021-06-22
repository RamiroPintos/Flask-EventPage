import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

load_dotenv(override=True)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.getenv('DB_CONNECTION') + '@localhost/db_test'
db = SQLAlchemy(app)
# Mail settings
app.config['MAIL_HOSTNAME'] = 'localhost'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SENDER'] = 'NDEAAH Eventos <ndeaah@noreply.com>'

email = Mail(app)  # Mail initialize
login_manager = LoginManager(app)
csrf = CSRFProtect(app)
app.secret_key = os.urandom(24)


def admin_required():
    return current_user.es_admin()


if __name__ == '__main__':
    from routes.routes import *
    from routes.api_routes import *
    from exceptions.exceptions import *

    app.run()
