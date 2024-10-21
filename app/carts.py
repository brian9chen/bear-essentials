from flask import render_template
from flask_login import current_user
import datetime
 
from .models.cart import Cart

from flask import Blueprint
from flask import jsonify
bp = Blueprint('index', __name__)


@bp.route('/carts')
def index():
    # get cart of current_user
    products = Product.get(current_user.id)
    if not current_user.is_authenticated:
        return jsonfiy({}), 404
    else:
        return jsonify([item.__dict__ for item in items])