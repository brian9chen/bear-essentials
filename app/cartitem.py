from flask import Blueprint, jsonify, render_template, flash, redirect, url_for
from flask_login import current_user
from .models.cartitem import CartItem
from .models.product import Product
from .models.review import Review

from flask import request, redirect, url_for

bp = Blueprint('cartitem', __name__)

@bp.route('/cartitem', methods=['GET'])
def cartitem():
    if current_user.is_authenticated:
        cart_items = CartItem.get_all_by_uid(current_user.id)
        total_price = sum(item['quantity'] * item['product_price'] for item in cart_items)
        return render_template('cartitem.html', cart_items=cart_items, total_price=total_price)
    else:
        return render_template('cartitem.html', cart_items=[], total_price=0.0)
    return jsonify({}), 404

# adds new cartitem and also brings you to your cart with added cartitem
@bp.route('/add/<int:id>', methods=['GET', 'POST'])
def add(id):
    if current_user.is_authenticated:
        # get product and associated creator id
        product = Product.get(id)
        creator_id = product.creator_id
        quantity = request.form.get('quantity')
        seller_name = request.form.get('seller_name')
        # ADD CORRECT VARIABLE INPUTS TO ADD
        added = CartItem.add(id, creator_id, current_user.id, quantity, seller_name)
        if added == "quantity too small":
            flash('Quantity must be 1 or larger.')
            return redirect(url_for('index.product_detail', id=id, page=1))
        if added == False:
            flash('Selected quantity exceeded quantity in stock for this product.')
            return redirect(url_for('index.product_detail', id=id, page=1))
        elif added == True:
            flash('Invalid Seller.')
            return redirect(url_for('index.product_detail', id=id, page=1))
        else:
            cart_items = CartItem.get_all_by_uid(current_user.id)
            total_price = sum(item['quantity'] * item['product_price'] for item in cart_items)
            return render_template('cartitem.html', cart_items=cart_items, total_price=total_price)
    else:
        return render_template('cartitem.html', cart_items=[], total_price=0.0)

@bp.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    CartItem.delete(id)
    return redirect(url_for('cartitem.cartitem'))

@bp.route('/change/<int:id>', methods=['GET','POST'])
def change(id):
    new_quantity = request.form.get('new_quantity')
    if not new_quantity.isdigit():
        flash('Invalid quantity.')
        return redirect(url_for('cartitem.cartitem'))
    if int(new_quantity) <= 0:
        flash('Quantity must be 1 or larger.')
    changed = CartItem.change(id, new_quantity)
    if changed == 'too little quantity':
        flash('Selected quantity exceeded quantity in stock for this product.')
    return redirect(url_for('cartitem.cartitem'))