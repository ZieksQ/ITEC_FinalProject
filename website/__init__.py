from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
db_name = "database.db"
login_manager = LoginManager()

def run_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    app.config['SECRET_KEY'] = 'd0a43f4b7e97cf2d2808fb86472c8724'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager.init_app(app)    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    db.init_app(app)
    
    from .views import views
    from .sorting_product import sorting_product
    from .delete_update_product import delete_update_product
    from .auth import auth
    from . import models
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(sorting_product, url_prefix='/sorted')
    app.register_blueprint(delete_update_product, url_prefix='/deleted_updated')
    app.register_blueprint(auth, url_prefix='/auth')

    create_database(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app

def create_database(app):
    if not path.exists('website/' + db_name):
        with app.app_context():
            db.create_all()
            print('Created Database!')
