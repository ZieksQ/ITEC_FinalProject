from flask import Blueprint, request, redirect, render_template, url_for, flash, get_flashed_messages
from website import db
from website.models import Product

delete_update_product = Blueprint('delete_update_product', __name__)

@delete_update_product.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Product.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('sorting_product.sorted_by_inventory'))
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to update product! error:{e}', category='error')
        return render_template('Inventory.html')
    finally:
        db.session.close()
    
@delete_update_product.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.product_name = request.form['product_name']
        product.price = request.form['price']
        product.stock = request.form['stock']
        product.manufacturer = request.form['manufacturer']
        product.category = request.form['category']

        # existing_product = Product.query.filter_by(product_name=product.product_name).first()

        try:
            db.session.commit()
            flash('Product updated successfully!', category='success')
            return redirect(url_for('views.add_product'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to update product! error:{e}', category='error')
            return render_template('Inventory.html', product=product)
        finally:
            db.session.close()

    else:
        return render_template('Inventory.html', product=product)

    