from flask import Blueprint, render_template, url_for
from website import db


views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
def home():
    
    
    return render_template("Inventory.html")