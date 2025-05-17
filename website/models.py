from website import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_iser(user_id):
    return User.query.get(int(user_id))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    manufacturer = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # def __repr__(self):
    #     return f'<Product {self.product_name}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # def __repr__(self):
    #     return f'<User {self.username}>'
    