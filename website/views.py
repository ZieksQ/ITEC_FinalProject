from flask import Blueprint, request, redirect, render_template, url_for
from website import db
from website.models import Product

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():
    
        if request.method == 'POST': 
            id = request.form.get('id')
            product_name = request.form['product_name']
            price = request.form['price']
            stock = request.form['stock']
            manufacturer = request.form['manufacturer']
            category = request.form['category']

            new_product = Product(id=id, product_name=product_name, price=price, stock=stock, manufacturer=manufacturer, category=category)
            
            try:
                db.session.add(new_product)
                db.session.commit()
                return redirect('/')
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
        return redirect('/')
    except:
        return "There was a problem deleting that task"
    
@views.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task = Product.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "You have failed to update the task"
    else:
        return render_template('testing.html', task=task)
    

def format_price(price):
    return f"₱{float(price):,.2f}"