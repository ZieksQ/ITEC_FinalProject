from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views import views

db = SQLAlchemy()
db_name = "database.db"

def run_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)
    

    app.register_blueprint(views, url_prefix='/')

    return app