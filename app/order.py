from flask import Blueprint, jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user
from .models.order import Order
from .models.cartitem import CartItem

bp = Blueprint('order', __name__)

@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    code = request.form.get("coupon_code")
    order_id = Order.submit(current_user.id, code)
    if order_id == True:
        flash('The quantity of an item in your cart exceeds the available quantity of this product.')
        return redirect(url_for('cartitem.cartitem'))
    if order_id == False:
        flash('The total price of this order exceeds your current balance.')
        return redirect(url_for('cartitem.cartitem'))
    cart_items = CartItem.get_items_by_order_id(order_id)
    discount = Order.get_discount(order_id)
    total_price = sum(item['quantity'] * float(item['product_price']) for item in cart_items) * (1-discount)
    return render_template('order.html', cart_items=cart_items, total_price=total_price, discount=discount)

@bp.route('/orders', methods=['GET', 'POST'])
def orders():
    orders = Order.get_orders_by_user(current_user.id)
    return render_template('orders.html', orders=orders)

@bp.route('/pastorder/<int:id>', methods=['GET'])
def pastorder(id):
    cart_items = CartItem.get_items_by_order_id(id)
    discount = Order.get_discount(id)
    total_price = sum(item['quantity'] * float(item['product_price']) for item in cart_items) * (1-discount)
    return render_template('order.html', cart_items=cart_items, total_price=total_price, discount=discount)