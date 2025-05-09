from flask import Blueprint, render_template, url_for


views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():

    return render_template("Inventory.html")