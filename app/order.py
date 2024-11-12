from flask import Blueprint, jsonify, render_template
from flask_login import current_user
from .models.order import Order
from .models.cartitem import CartItem

bp = Blueprint('order', __name__)


@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    cart_items = CartItem.get_all_by_uid(current_user.id)
    total_price = sum(item['quantity'] * item['product_price'] for item in cart_items)
    Order.submit(current_user.id, total_price)
    return render_template('order.html', cart_items=cart_items, total_price=total_price)