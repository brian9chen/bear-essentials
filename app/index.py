from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime
import pandas as pd
 
from .models.product import Product
from .models.purchase import Purchase
from .models.review import Review
from .models.inventory import Inventory

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

    # Redirect to user profile if user_id is provided in the URL
    user_id = request.args.get('user_id', type=int)
    if user_id:
        return redirect(url_for('users.public_view', user_id=user_id))

    # Fetch categories for filtering
    categories = Product.get_categories()

    # Handle sorting, filtering, and keyword search 
    sort_order = request.form.get('sort_order')  or request.args.get('sort_order')
    selected_category = request.form.get('category', '') or request.args.get('category', '')
    keyword = request.form.get('keyword', '', type=str) or request.args.get('keyword', '', type=str)

    products = Product.sort_and_filter(category=selected_category, sort_order=sort_order, keyword=keyword)

    # Implement pagination
    PRODUCTS_PER_PAGE = 24
    page = request.args.get('page', 1, type=int)
    total_products = len(products)
    total_pages = (total_products + PRODUCTS_PER_PAGE - 1) // PRODUCTS_PER_PAGE
    start_index = (page - 1) * PRODUCTS_PER_PAGE
    end_index = start_index + PRODUCTS_PER_PAGE
    products_in_page = products[start_index:end_index]

    # Render the page with relevant information
    return render_template('index.html', avail_products=products_in_page, purchase_history=purchases, 
                           categories=categories, sort_order=sort_order, selected_category=selected_category,
                           keyword=keyword, page=page, total_pages=total_pages)

@bp.route('/most_expensive_products', methods=('GET', 'POST'))
def top_k():
    if request.method == 'POST':
        k = request.form.get('k', type=int)
        products = Product.most_expensive_products(k)
        return render_template('index.html', avail_products=products)
    return render_template('index.html')

@bp.route('/product/<int:id>', methods=['GET'])
def product_detail(id):
    # Fetch the product by ID from the database
    product = Product.get(id)
    if not product:
        # Handle case if product is not found
        abort(404)


    sellers_list = Product.get_sellers(id)


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

    return render_template('product.html', 
                           product=product, 
                           sellers=sellers_list,
                           reviews=reviews, 
                           page=page, 
                           total_pages=total_pages)

@bp.route('/view_user_profile', methods=['POST'])
def view_user_profile():
    user_id = request.form.get('user_id', type=int)
    if user_id:
        return redirect(url_for('users.public_view', user_id=user_id))
    return redirect(url_for('index.index'))  # Redirect back to index if no user_id is provided