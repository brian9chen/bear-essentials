from flask import Blueprint, jsonify, request, render_template
from .models.product import Product
from .models.purchase import Purchase
from .models.user import User
from flask_login import current_user

bp = Blueprint('purchases', __name__)

@bp.route('/purchases', methods=['GET', 'POST'])
def purchases():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
    else:
        user_id = request.args.get('user_id')

    if user_id:
        user = User.get(user_id)
        if not user:
            return render_template('purchases.html', error="User not found")
    elif current_user.is_authenticated:
        user = current_user
    else:
        user = None
    
    # purchases = Purchase.get_all_by_id(user.id)
    
    # # Fetch product information for each purchase
    # for purchase in purchases:
    #     purchase.product = Product.get(purchase.pid)

    purchases = []
    if user:
        purchases = Purchase.get_all_by_id(user.id)
        
        # Fetch product information for each purchase
        for purchase in purchases:
            purchase.product = Product.get(purchase.pid)
    
    return render_template('purchases.html', purchases=purchases, user=user)

@bp.route('/api/user_purchases', methods=['GET'])
def get_user_purchases():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    purchased_products = Product.getPurchasesProducts(user_id)
    return jsonify(purchased_products)
