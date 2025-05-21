from flask import Blueprint, request, redirect, render_template, url_for, flash, get_flashed_messages
from website import db
from website.models import Product
from flask_login import login_required, logout_user, current_user
from .auth import UpdateForm

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
def home():

    return render_template("Homepage.html")

@views.route('/logout', methods=['POST', 'GET'])
def logout():

    logout_user()
    
    flash('You have been logged out!', category='success')
    return render_template("Homepage.html")

@views.route('/contacts')
def contacts():

    return render_template("contacts.html")

@views.route('/inventory', methods=['POST', 'GET'])
@login_required
def add_product():
    if request.method == 'POST': 
            id = request.form.get('id')
            product_name = request.form.get('product_name')
            price = request.form.get('price')
            stock = request.form.get('stock')
            manufacturer = request.form.get('manufacturer')
            category = request.form.get('category')

            existing_product = Product.query.filter_by(product_name=product_name).first()

            if existing_product:
                flash('Product already exists!.', category='error')
                return redirect('/inventory')
            else:
                new_product = Product(id=id, product_name=product_name, price=price, stock=stock, manufacturer=manufacturer, category=category)

                try:
                    db.session.add(new_product)
                    db.session.commit()
                    flash('Product added successfully!', category='success')
                    return redirect('/inventory')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Failed to add product! error:{e}', category='error')
                    return redirect('/inventory')
                
    else:
        products = Product.query.order_by(Product.date_created).all()
        return render_template("Inventory.html", products=products, format_price=format_price)
        
@views.route('/search', methods=['POST', 'GET'])
def search():
    
    querry = request.args.get('search', 'Nothing')

    if querry:
        searches = Product.query.filter(
            Product.product_name.ilike(f'%{querry}%') | Product.manufacturer.ilike(f'%{querry}%') | Product.category.ilike(f'%{querry}%')
            ).order_by(Product.id.asc()).limit(100).all()
        if not searches:
            searches = Product.query.all()
            flash("No product found!", category='error')
    else:
        flash('No product found!', category='error')
        searches = Product.query.all()

    return render_template('search.html', searches=searches, format_price=format_price)

def format_price(price):
    return f"₱{float(price):,.2f}"





@views.route('/Terms of Service')
def tos():
    return render_template('tos.html')
@views.route('/Privacy Policy')
def privacy():
    return render_template('privacy_policy.html')
