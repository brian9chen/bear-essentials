from flask import Blueprint, jsonify, request, render_template
from .models.product import Product
from flask_login import login_required

bp = Blueprint('purchases', __name__)

@bp.route('/api/user_purchases', methods=['GET'])
def get_user_purchases():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    purchased_products = Product.getPurchasesProducts(user_id)
    return jsonify(purchased_products)

@bp.route('/purchases')
def purchases():
    return render_template('purchases.html')
