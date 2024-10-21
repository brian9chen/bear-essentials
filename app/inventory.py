from flask import Blueprint, jsonify
from flask_login import current_user
from .models.inventory import Inventory

bp = Blueprint('inventory', __name__)

@bp.route('/inventory', methods=['GET'])
def inventory():
    """Retrieve all inventory items for the current logged-in user (merchant)."""
    if current_user.is_authenticated:
        inventory_items = Inventory.get_all_by_user(current_user.id)
        return jsonify(inventory_items)
    return jsonify({}), 404