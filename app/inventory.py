from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app as app
from flask_login import current_user
import os
from werkzeug.utils import secure_filename
from .models.inventory import Inventory
from .models.product import Product

bp = Blueprint('inventory', __name__)

@bp.route('/inventory', methods=['GET'])
def inventory():
    if current_user.is_authenticated:
        inventory_items = Inventory.get_all_by_user(current_user.id)
        categories = Product.get_unique_categories()  # Fetch unique categories
        return render_template('inventory.html', inventory_items=inventory_items, categories=categories)
    
    return jsonify({}), 404

@bp.route('/inventory/add', methods=['POST'])
def add_product():
    if current_user.is_authenticated:
        product_name = request.form.get('product_name')
        quantity = request.form.get('quantity_in_stock', type=int)
        price = request.form.get('price')  # Optional for existing products
        category = request.form.get('category')
        description = request.form.get('description')  # Optional for existing products

        # Add the product to the user's inventory
        Inventory.add_product(current_user.id, product_name, quantity, price, category, description)
        return redirect(url_for('inventory.inventory'))
    return jsonify({}), 404

@bp.route('/inventory/update/<int:inventory_id>', methods=['POST'])
def update_quantity(inventory_id):
    if current_user.is_authenticated:
        new_quantity = request.form.get('new_quantity', type=int)

        if new_quantity is None:
            return "New quantity is required and must be a valid integer", 400

        Inventory.update_quantity(inventory_id, new_quantity)
        return redirect(url_for('inventory.inventory'))
    return jsonify({}), 404

@bp.route('/inventory/remove/<int:inventory_id>', methods=['POST'])
def remove_product(inventory_id):
    if current_user.is_authenticated:
        Inventory.remove_product(inventory_id)
        return redirect(url_for('inventory.inventory'))
    return jsonify({}), 404

@bp.route('/inventory/update_price/<int:inventory_id>', methods=['POST'])
def update_price(inventory_id):
    if current_user.is_authenticated:
        new_price = request.form.get('new_price', type=float)
        if new_price is None:
            return "New price is required and must be a valid number", 400
        Inventory.update_price(inventory_id, new_price)
        
        return redirect(url_for('inventory.inventory'))
    return jsonify({}), 404

@bp.route('/inventory/update_description/<int:inventory_id>', methods=['POST'])
def update_description(inventory_id):
    if current_user.is_authenticated:
        new_description = request.form.get('new_description')
        
        Inventory.update_description(inventory_id, new_description)
        return redirect(url_for('inventory.inventory'))
    return jsonify({}), 404

@bp.route('/inventory/update_category/<int:inventory_id>', methods=['POST'])
def update_category(inventory_id):
    if current_user.is_authenticated:
        new_category = request.form.get('new_category')

        Inventory.update_category(inventory_id, new_category)
        return redirect(url_for('inventory.inventory'))
    return jsonify({}), 404

@bp.route('/inventory/update_name/<int:inventory_id>', methods=['POST'])
def update_name(inventory_id):
    if current_user.is_authenticated:
        new_name = request.form.get('new_name')

        Inventory.update_name(inventory_id, new_name)
        return redirect(url_for('inventory.inventory'))
    return jsonify({}), 404


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/inventory/update_image/<int:inventory_id>', methods=['POST'])
def update_image(inventory_id):
    if 'image' not in request.files:
        return redirect(request.referrer or url_for('inventory.inventory'))
    
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Full file path
        file.save(filepath)  # Save file to static/uploads/

        # Save the relative path "uploads/<filename>" in the database
        Inventory.update_image_path(inventory_id, os.path.join('uploads', filename))

    return redirect(request.referrer or url_for('inventory.inventory'))

@bp.route('/inventory/search', methods=['GET'])
def search_products():
    query = request.args.get('query', '').strip()
    if not query:
        return render_template('inventory.html', inventory_items=Inventory.get_all_by_user(current_user.id), categories=Product.get_unique_categories(), search_results=[])

    results = Product.search(query)  # Assumes a Product.search(query) method
    return render_template('inventory.html', inventory_items=Inventory.get_all_by_user(current_user.id), categories=Product.get_unique_categories(), search_results=results)



