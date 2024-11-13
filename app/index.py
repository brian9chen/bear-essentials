from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime
 
from .models.product import Product
from .models.purchase import Purchase
from .models.review import Review

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

    user_id = request.args.get('user_id', type=int)
    if user_id:
        return redirect(url_for('users.public_view', user_id=user_id))

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

    # Fetch all reviews for the given product ID, sorted by upvotes
    all_reviews = Review.get_sortedByUpvote_by_pid(id)

    # Define the number of reviews per page
    REVIEWS_PER_PAGE = 10

    # Get the page number from the request (default to 1 if not specified)
    page = request.args.get('page', 1, type=int)

    # Calculate start and end indices for the current page
    start_index = (page - 1) * REVIEWS_PER_PAGE
    end_index = start_index + REVIEWS_PER_PAGE

    # Slice the list to get only the reviews for the current page
    reviews = all_reviews[start_index:end_index]

    # Calculate total pages based on the number of reviews
    total_reviews = len(all_reviews)
    total_pages = (total_reviews + REVIEWS_PER_PAGE - 1) // REVIEWS_PER_PAGE  # Round up for any remainder

    return render_template('product.html', product=product, reviews=reviews, page=page, total_pages=total_pages)

@bp.route('/view_user_profile', methods=['POST'])
def view_user_profile():
    user_id = request.form.get('user_id', type=int)
    if user_id:
        return redirect(url_for('users.public_view', user_id=user_id))
    return redirect(url_for('index.index'))  # Redirect back to index if no user_id is provided