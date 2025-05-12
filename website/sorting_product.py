from flask import Blueprint, request, redirect, render_template, url_for, flash, get_flashed_messages
from website.models import Product

sorting_product = Blueprint('sorting_product', __name__)

@sorting_product.route('/inventory_sorted_by_the_stock', methods=['POST', 'GET'])
def sorted_by_inventory():

    sort = request.args.get('sort', 'prodcut_name')
    order = request.args.get('order', 'asc')

    columnstock = getattr(Product, sort, Product.stock)
    columnid = getattr(Product, sort, Product.id)

    if order == 'desc_stock':
        products = Product.query.order_by(columnstock.desc()).all()
    elif order == 'asc_stock':
        products = Product.query.order_by(columnstock.asc()).all()
    elif order == 'desc_price':
        products = Product.query.order_by(columnid.desc()).all()
    elif order == 'asc_price':
        products = Product.query.order_by(columnid.asc()).all()
    else:
        products = Product.query.order_by(columnstock.asc()).all()
        products = Product.query.order_by(columnid.asc()).all()

    for product in products:
            product.price = format_price(product.price)

    return render_template('Inventory.html', products=products, order=order, sort=sort)

@sorting_product.route('/search_sorted_by_the_stock', methods=['POST', 'GET'])
def sorted_by_search():

    sort = request.args.get('sort', 'prodcut_name')
    order = request.args.get('order', 'asc')

    columnstock = getattr(Product, sort, Product.stock)
    columnid = getattr(Product, sort, Product.id)
    
    if order == 'desc_stock':
        searches = Product.query.order_by(columnstock.desc()).all()
    elif order == 'asc_stock':
        searches = Product.query.order_by(columnstock.asc()).all()
    elif order == 'desc_price':
        searches = Product.query.order_by(columnid.desc()).all()
    elif order == 'asc_price':
        searches = Product.query.order_by(columnid.asc()).all()
    else:
        searches = Product.query.order_by(columnstock.asc()).all()
        searches = Product.query.order_by(columnid.asc()).all()

    for product in searches:
            product.price = format_price(product.price)

    return render_template('search.html', searches=searches, order=order, sort=sort)

def format_price(price):
    return f"₱{float(price):,.2f}"