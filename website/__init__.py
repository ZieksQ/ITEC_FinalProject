from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
db_name = "database.db"

def run_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)
    
    from .views import views

    app.register_blueprint(views, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not path.exists('website/' + db_name):
        db.create_all(app=app)
        print('Created Database!')