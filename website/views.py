from flask import Blueprint, request, redirect, render_template, url_for, flash, get_flashed_messages
from website import db
from website.models import Product

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
def home():

    return render_template("Homepage.html")

@views.route('/profile', methods=['POST', 'GET'])    
def the_profile():

    return render_template("profile.html")
        
@views.route('/inventory', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST': 
            id = request.form.get('id')
            product_name = request.form['product_name']
            price = request.form['price']
            stock = request.form['stock']
            manufacturer = request.form['manufacturer']
            category = request.form['category']

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
    query = request.args.get('search')
    print(query)

    if query:
        searches = Product.query.filter(
            Product.product_name.ilike(f'%{query}%') | Product.manufacturer.ilike(f'%{query}%')
            ).order_by(Product.id.asc()).limit(100).all()

    else:
        flash('No product found!', category='error')
        searches = Product.query.all()

    return render_template('search.html', searches=searches, format_price=format_price)

def format_price(price):
    return f"₱{float(price):,}"
