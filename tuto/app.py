import os.path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), p))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + mkpath('myapp.db')
app.config['SECRET_KEY'] = 'votre_clé_secrète_unique'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

