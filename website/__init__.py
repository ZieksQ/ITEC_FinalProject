from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
db_name = "database.db"

def run_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    app.config['SECRET_KEY'] = 'd0a43f4b7e97cf2d2808fb86472c8724'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from .views import views
    from .sorting_product import sorting_product
    from .delete_update_product import delete_update_product
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(sorting_product, url_prefix='/sorted')
    app.register_blueprint(delete_update_product, url_prefix='/deleted_updated')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not path.exists('website/' + db_name):
        db.create_all(app=app)
        print('Created Database!')
