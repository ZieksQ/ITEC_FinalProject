from flask import Blueprint, request, redirect, render_template, url_for, flash, get_flashed_messages
from website.models import Product
from website.views import format_price

sorting_product = Blueprint('sorting_product', __name__)

@sorting_product.route('/inventory_sorted_by_the_stock', methods=['GET'])
def sorted_by_inventory():

    sort = request.args.get('sort', 'product_name')
    order = request.args.get('order', 'asc')

    columnid = getattr(Product, sort, Product.id)
    columnname = getattr(Product, sort, Product.product_name)
    columnprice  = getattr(Product, sort, Product.price)
    columnstock = getattr(Product, sort, Product.stock)
    columnmanufacturer = getattr(Product, sort, Product.manufacturer)
    columncategory = getattr(Product, sort, Product.category)
    columncreated = getattr(Product, sort, Product.date_created)
    columnupdated = getattr(Product, sort, Product.date_updated)

    if order == 'desc_id':
        column = columnid.desc()
    elif order == 'asc_id':
        column = columnid.asc()
    elif order == 'desc_name':
        column = columnname.desc()
    elif order == 'asc_name':
        column = columnname.asc()
    elif order == 'desc_price':
        column = columnprice.desc()
    elif order == 'asc_price':
        column = columnprice.asc()
    elif order == 'desc_stock':
        column = columnstock.desc()
    elif order == 'asc_stock':
        column = columnstock.asc()
    elif order == 'desc_manufacturer':
        column = columnmanufacturer.desc()
    elif order == 'asc_manufacturer':
        column = columnmanufacturer.asc()
    elif order == 'desc_category':
        column = columncategory.desc()
    elif order == 'asc_category':
        column = columncategory.asc()
    elif order == 'desc_created':
        column = columncreated.desc()
    elif order == 'asc_created':
        column = columncreated.asc()
    elif order == 'desc_updated':
        column = columnupdated.desc()
    elif order == 'asc_updated':
        column = columnupdated.asc()
    else:
        column = columnid.asc()

    products = Product.query.order_by(column).all()

    return render_template('Inventory.html', products=products, order=order, sort=sort, format_price=format_price)

@sorting_product.route('/search_sorted_by_the_stock', methods=['POST', 'GET'])
def sorted_by_search():

    sort = request.args.get('sort', 'product_name')
    order = request.args.get('order', 'asc')

    columnid = getattr(Product, sort, Product.id)
    columnname = getattr(Product, sort, Product.product_name)
    columnprice  = getattr(Product, sort, Product.price)
    columnstock = getattr(Product, sort, Product.stock)
    columnmanufacturer = getattr(Product, sort, Product.manufacturer)
    columncategory = getattr(Product, sort, Product.category)
    columncreated = getattr(Product, sort, Product.date_created)
    columnupdated = getattr(Product, sort, Product.date_updated)

    if order == 'desc_id':
        column = columnid.desc()
    elif order == 'asc_id':
        column = columnid.asc()
    elif order == 'desc_name':
        column = columnname.desc()
    elif order == 'asc_name':
        column = columnname.asc()
    elif order == 'desc_price':
        column = columnprice.desc()
    elif order == 'asc_price':
        column = columnprice.asc()
    elif order == 'desc_stock':
        column = columnstock.desc()
    elif order == 'asc_stock':
        column = columnstock.asc()
    elif order == 'desc_manufacturer':
        column = columnmanufacturer.desc()
    elif order == 'asc_manufacturer':
        column = columnmanufacturer.asc()
    elif order == 'desc_category':
        column = columncategory.desc()
    elif order == 'asc_category':
        column = columncategory.asc()
    elif order == 'desc_created':
        column = columncreated.desc()
    elif order == 'asc_created':
        column = columncreated.asc()
    elif order == 'desc_updated':
        column = columnupdated.desc()
    elif order == 'asc_updated':
        column = columnupdated.asc()
    else:
        column = columnid.asc()

    searches = Product.query.order_by(column).all()

    return render_template('search.html', searches=searches, order=order, sort=sort, format_price=format_price)
