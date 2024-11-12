from flask import render_template
from flask_login import current_user
import datetime
 
from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__)

from flask import request 

# change avail_products??

@bp.route('/', methods=['GET', 'POST'])
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file

    # add filter by category 
    categories = Product.get_categories()  # Fetch 
    selected_category = request.form.get('category')  # Get 

    if selected_category:
        products = Product.filter_by_category(selected_category)
    else:
        products = Product.get_all()  # Show all products by default 

    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           categories=categories,
                           selected_category=selected_category)

@bp.route('/most_expensive_products', methods=('GET', 'POST'))
def top_k():
    if request.method == 'POST':
        k = request.form.get('k', type=int)
        products = Product.most_expensive_products(k)
        return render_template('index.html', avail_products=products)
    return render_template('index.html')

@bp.route('/filter_by_keyword', methods=('GET', 'POST'))
def search_keyword():
    if request.method == 'POST':
        keyword = request.form.get('keyword', type=str)
        products = Product.filter_by_keyword(keyword)
        return render_template('index.html', avail_products=products)
    return render_template('index.html')

#  sort by price 
@bp.route('/sort/<string:sort_order>', methods=['GET'])
def sort_by_price(sort_order):
    # Fetch products from the database
    if sort_order == 'asc':
        products = Product.sort_by_price_asc()  # Sort by price ascending
    else:
        products = Product.sort_by_price_desc()  # Sort by price descending
    
    # Return the sorted products to the template
    return render_template('index.html', avail_products=products, sort_order=sort_order)

@bp.route('/product/<int:id>', methods=['GET'])
def product_detail(id):
    # Fetch the product by ID from the database
    product = Product.get(id)
    if not product:
        # Handle case if product is not found
        abort(404)

    return render_template('product.html', product=product)