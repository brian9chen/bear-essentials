from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from .models.order import Order
from .models.cartitem import CartItem

bp = Blueprint('fulfillment', __name__)

@bp.route('/fulfillment', methods=['GET'])
def seller_fulfillment():
    seller_id = current_user.id
    search = request.args.get("search", None)
    status_filter = request.args.get("status_filter", "all")  # Default to 'all' if not provided
    orders = Order.get_seller_orders_with_items(seller_id, search=search, status_filter=status_filter)
    return render_template('seller_fulfillment.html', orders=orders, search=search, status_filter=status_filter)



@bp.route('/fulfillment/mark_fulfilled/<int:cartitem_id>', methods=['POST'])
def fulfill_cartitem(cartitem_id):
    CartItem.mark_as_fulfilled(cartitem_id)
    return redirect(request.referrer or url_for('fulfillment.seller_fulfillment'))
