# from flask import Flask, Blueprint, request, redirect, render_template
# from website import db
# from website.models import Product
# from wtforms.validators import DataRequired
# from wtforms import StringField, IntegerField
# from flask_wtf import FlaskForm

# add_products = Blueprint('add_Products', __name__)

# class Product_Validation(FlaskForm):
#     product_name = StringField('product_name', validators=[DataRequired()])
#     price = IntegerField('price', validators=[DataRequired()])
#     stock = IntegerField('stock', validators=[DataRequired()])
#     manufacturer = StringField('manufacturer', validators=[DataRequired()])
#     category = StringField('Category', validators=[DataRequired()])

# @add_products.route('/add_product', methods=['POST', 'GET'])
# def add_product():

#     form = Product_Validation()

#     if request.method == 'POST' and form.validate_on_submit(): 
            
#             """
#             id = request.form.get('id')
#             product_name = request.form['product_name']
#             price = request.form['price']
#             stock = request.form['stock']
#             manufacturer = request.form['manufacturer']
#             category = request.form['category']
#             """

#             product_name = form.product_name.data()
#             price = form.price.data()
#             stock = form.stock.data()
#             manufacturer = form.manufacturer.data()
#             category = form.category.data()

#             new_product = Product(id=id, product_name=product_name, price=price, stock=stock, manufacturer=manufacturer, category=category)
            
#             try:
#                 db.session.add(new_product)
#                 db.session.commit()
#                 return redirect('/')
#             except:
#                 return "There was an issue adding your product"

#     else:
#         products = Product.query.order_by(Product.date_created).all()
#         for product in products:
#             product.price = format_price(product.price)
#             return render_template("Inventory.html", products=products)


# def format_price(price):
#     return f"₱{float(price):,.2f}"