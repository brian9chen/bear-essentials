from flask import Blueprint, jsonify, render_template
from flask_login import current_user
from .models.cartitem import CartItem

bp = Blueprint('cartitem', __name__)

@bp.route('/cartitem', methods=['GET'])
def cartitem():
    if current_user.is_authenticated:
        cart_items = CartItem.get_all_by_uid(current_user.id)
        total_price = sum(item['quantity'] * item['product_price'] for item in cart_items)
        return render_template('cartitem.html', cart_items=cart_items, total_price=total_price)
    return jsonify({}), 404