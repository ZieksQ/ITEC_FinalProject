from flask import Blueprint, request, redirect, render_template, url_for, flash, get_flashed_messages
from website import db
from website.models import Product

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
def home():

    return render_template("setting.html")

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
                except:
                    return "There was an issue adding your product"
    else:
        products = Product.query.order_by(Product.date_created).all()
        for product in products:
            product.price = format_price(product.price)
        return render_template("Inventory.html", products=products)
        
@views.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Product.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/inventory')
    except:
        return "There was a problem deleting that task"
    
@views.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.product_name = request.form['product_name']
        product.price = request.form['price']
        product.stock = request.form['stock']
        product.manufacturer = request.form['manufacturer']
        product.category = request.form['category']

        try:
            db.session.commit()
            return redirect('/inventory')
        except:
            return "You have failed to update the task"
    else:
        return render_template('Inventory.html', product=product)
    
@views.route('/search', methods=['POST', 'GET'])
def search():
    query = request.args.get('search')
    print(query)

    if query:
        searches = Product.query.filter(Product.product_name.ilike(f'%{query}%') | Product.manufacturer.ilike(f'%{query}%')).order_by(Product.id.asc()).limit(100).all()

    else:
        flash('No product found!', category='error')
        searches = Product.query.all()
        
    return render_template('search.html', searches=searches)

<<<<<<< HEAD
@views.route('/sorting', methods=['POST', 'GET'])
def sort_by_id():
    sortedproducts = Product.query.order_by(Product.id.desc()).all()
    return render_template('Inventory.html', sortedproducts=sortedproducts)
=======
@views.route('/inventory_sorted_by_the_stock', methods=['POST', 'GET'])
def sorted_by():
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

    return render_template('Inventory.html', products=products, order=order, sort=sort)
>>>>>>> 9008a3101b3162bb2590db2488d4d5b9c9d936c2

def format_price(price):
    return f"₱{float(price):,.2f}"