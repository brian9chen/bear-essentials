from flask import Blueprint, jsonify, request, render_template
from .models.purchase import Purchase
from flask_login import login_required

bp = Blueprint('purchases', __name__)

@bp.route('/api/user_purchases', methods=['GET'])
def get_user_purchases():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    


    purchases = Purchase.get_by_uid(user_id)
    return jsonify([purchase.to_dict() for purchase in purchases])
    # except Exception as e:
    #     current_app.logger.error(f"Error fetching purchases for user {user_id}: {e}")
    #     return jsonify({"error": "An error occurred while fetching the data"}), 500

@bp.route('/purchases')
def purchases():
    return render_template('purchases.html')
