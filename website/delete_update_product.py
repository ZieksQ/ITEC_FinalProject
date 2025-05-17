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
        flash("Product delete succesfully", category='error')
        return redirect(url_for('sorting_product.sorted_by_inventory'))
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to update product! error:{e}', category='error')
        return render_template('Inventory.html')

@delete_update_product.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.product_name = request.form.get('product_name')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.manufacturer = request.form.get('manufacturer')
        product.category = request.form.get('category')

        existing_product = Product.query.filter(Product.product_name.ilike(product.product_name), Product.id != id).first()

        if existing_product:
            flash('Product with this name already exists!', category='error')
            return redirect(url_for('views.add_product'))

        else:
            try:
                db.session.commit()
                flash('Product updated successfully!', category='success')
                return redirect(url_for('views.add_product'))
            except Exception as e:
                db.session.rollback()
                flash(f'Failed to update product! error:{e}', category='error')
                return render_template('Inventory.html', product=product)
            
    else:
        return render_template('Inventory.html', product=product)
    
@delete_update_product.route('/delete_in_search/<int:id>')
def delete_in_search(id):
    task_to_delete = Product.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash('Product deleted successfully!', category='success')
        return redirect(url_for('sorting_product.sorted_by_search'))
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to update product! error:{e}', category='error')
        return render_template('search.html')

@delete_update_product.route('/update_in_search/<int:id>', methods=['GET', 'POST'])
def update_in_search(id):

    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.product_name = request.form.get('product_name')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.manufacturer = request.form.get('manufacturer')
        product.category = request.form.get('category')

        with db.session.no_autoflush:
            existing_product = Product.query.filter(Product.product_name.ilike(product.product_name), Product.id != id).first()

        if existing_product:
            flash('Product with this name already exists!', category='error')
            return render_template('search.html')

        else:
            try:
                db.session.commit()
                flash('Product updated successfully!', category='success')
                return redirect(url_for('sorting_product.sorted_by_search'))
            except Exception as e:
                db.session.rollback()
                flash(f'Failed to update product! error:{e}', category='error')
                return render_template('search.html', product=product)
            
    else:
        return render_template('search.html', product=product)
