from flask import Flask, Blueprint, request, render_template, url_for, redirect
from .models import Product
from website import db

add_products = Blueprint('add_products', __name__)

@add_products.route('/add_product', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        manufacturer = request.form.get('manufacturer')

        new_product = Product(product_name=product_name, price=price, stock=stock, manufacturer=manufacturer)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('views.home'))
        except:
            return "There was an issue adding the product"
        
    else:
        products = Product.query.order_by(Product.date_created).all()
        return render_template('Inventory.html', products=products)