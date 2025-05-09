from flask import Blueprint, request, redirect, render_template, url_for
from website import db
from website.models import Product


views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():
    
        if request.method == 'POST': 
            id = request.form['id']
            product_name = request.form['product_name']
            price = request.form['price']
            stock = request.form['stock']
            manufacturer = request.form['manufacturer']

            new_product = Product(id=id, product_name=product_name, price=price, stock=stock, manufacturer=manufacturer)
            
            try:
                db.session.add(new_product)
                db.session.commit()
                return redirect('/')
            except:
                return "There was an issue adding your product"

        else:
            products = Product.query.order_by(Product.date_created).all()
            return render_template("Inventory.html", products=products)

