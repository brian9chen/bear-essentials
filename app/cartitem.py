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

# from flask import jsonify, url_for, redirect, render_template
# from flask_login import current_user
# import datetime
# from humanize import naturaltime

# from .models.cartitem import CartItem

# from flask import Blueprint
# from flask import jsonify
# bp = Blueprint('cartitem', __name__)


# def humanize_time(dt):
#     return naturaltime(datetime.datetime.now() - dt)


# @bp.route('/cart', methods=['GET'])
# def cart():
#     if current_user.is_authenticated:
#         items = Cart.get_all_by_uid(
#             current_user.id)
#         return jsonify([item.__dict__ for item in items])
#     else:
#         return jsonify({}), 404

