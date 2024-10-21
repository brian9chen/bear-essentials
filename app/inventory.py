from flask import Blueprint, jsonify, render_template
from flask_login import current_user
from .models.inventory import Inventory

bp = Blueprint('inventory', __name__)

@bp.route('/inventory', methods=['GET'])
def inventory():
    if current_user.is_authenticated:
        inventory_items = Inventory.get_all_by_user(current_user.id)
        return render_template('inventory.html', inventory_items=inventory_items)
    
    return jsonify({}), 404