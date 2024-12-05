from flask import render_template, redirect, url_for
from flask import current_app as app
from flask_login import current_user
import datetime
import pandas as pd
import csv
 
from .models.product import Product
from .models.purchase import Purchase
from .models.review import Review
from .models.user import User
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

    total_products = len(products)
    product_ratings = {product.id: Review.get_avg_rating_by_pid(product.id) for product in products}
    best_seller_ids = Product.get_best_seller_ids()

    if sort_order == 'best_seller':
        products = sorted(products, key=lambda p: best_seller_ids.index(p.id) if p.id in best_seller_ids else float('inf'))
    elif sort_order == 'rating_desc':
        products.sort(key=lambda p: product_ratings.get(p.id) or 0, reverse=True)
    elif sort_order == 'rating_asc':
        products.sort(key=lambda p: product_ratings.get(p.id) or 0)

    p10 = max(1, int(len(best_seller_ids) * 0.10))
    best_seller_ids_p10 = best_seller_ids[:p10]

    # Implement pagination
    PRODUCTS_PER_PAGE = 24
    page = request.args.get('page', 1, type=int)
    total_products = len(products)
    total_pages = (total_products + PRODUCTS_PER_PAGE - 1) // PRODUCTS_PER_PAGE
    start_index = (page - 1) * PRODUCTS_PER_PAGE
    end_index = start_index + PRODUCTS_PER_PAGE
    products_in_page = products[start_index:end_index]
    
    if current_user.is_authenticated:
        for product in products_in_page:
            review = Review.has_user_reviewed_product(current_user.id, product.id)
            setattr(product, 'has_review', bool(review))
            setattr(product, 'review_id', review[0] if review else None)
    else:
        for product in products_in_page:
            setattr(product, 'has_review', False)
            setattr(product, 'review_id', None)

    coupons = []
    discounts = []

    with open('db/customized/Coupons.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            coupons.append(row[1])
            discounts.append(row[2])

    
    selected_coupon = coupons[0] if coupons else "NOCOUPON" 
    selected_discount = f"{float(discounts[0]) * 100:.0f}%" if coupons else "NODISCOUNT" 


    # Render the page with relevant information
    return render_template('index.html', avail_products=products_in_page, purchase_history=purchases, 
                           categories=categories, sort_order=sort_order, selected_category=selected_category,
                           keyword=keyword, page=page, total_pages=total_pages, product_ratings=product_ratings,
                           best_seller_ids_p10=best_seller_ids_p10, selected_coupon=selected_coupon, selected_discount=selected_discount)

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

    product_rating = Review.get_avg_rating_by_pid(product.id)

    sellers_list = Product.get_sellers(id)

    # Define pagination constants for sellers
    SELLERS_PER_PAGE = 5
    REVIEWS_PER_PAGE = 10

    # Get both page numbers from request
    page = request.args.get('page', 1, type=int)
    seller_page = request.args.get('seller_page', 1, type=int)

    # Get all sellers and paginate
    sellers_list = Product.get_sellers(id)
    total_sellers = len(sellers_list)
    seller_total_pages = (total_sellers + SELLERS_PER_PAGE - 1) // SELLERS_PER_PAGE
    seller_start = (seller_page - 1) * SELLERS_PER_PAGE
    seller_end = seller_start + SELLERS_PER_PAGE
    sellers_in_page = sellers_list[seller_start:seller_end]

    # Fetch all reviews for the given product ID, sorted by upvotes
    all_reviews = Review.get_sortedByUpvote_by_pid(id)
    
    for review in all_reviews:
        user = User.get(review.user_id)
        review.user_firstname = user.firstname
        review.user_lastname = user.lastname

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
    
    # get num reviews and avg rating
    num_reviews = len(all_reviews)
    product_rating = Review.get_avg_rating_by_pid(product.id)
    
    # check if user has reviewed product
    if current_user.is_authenticated:
        review = Review.has_user_reviewed_product(current_user.id, product.id)
        setattr(product, 'has_review', bool(review))
        setattr(product, 'review_id', review[0] if review else None)
    else:
        setattr(product, 'has_review', False)
        setattr(product, 'review_id', None)
    
    # check if user has reviewed sellers and/or purchased from sellers
    if current_user.is_authenticated:
        for seller in sellers_list:
            review = Review.has_user_reviewed_seller(current_user.id, seller['id'])
            has_purchased = User.has_purchased_from_seller(current_user.id, seller['id'])
            seller['has_review'] = bool(review)
            seller['review_id'] = review[0] if review else None
            seller['has_purchased'] = has_purchased
    else:
        for seller in sellers_list:
            seller['has_review'] = False
            seller['review_id'] = None
            seller['has_purchased'] = False
    
    if current_user.is_authenticated:
        for review in reviews:
            review.user_vote = Review.get_user_vote(current_user.id, review.id)
    else:
        for review in reviews:
            review.user_vote = 0

    return render_template('product.html',
                         product=product,
                         sellers=sellers_in_page,
                         seller_page=seller_page,
                         seller_total_pages=seller_total_pages,
                         reviews=reviews,
                         page=page,
                         total_pages=total_pages,
                         num_reviews=num_reviews,
                         product_rating=product_rating,
                         sellers_list=sellers_list)

@bp.route('/view_user_profile', methods=['POST'])
def view_user_profile():
    user_id = request.form.get('user_id', type=int)
    if user_id:
        return redirect(url_for('users.public_view', user_id=user_id))
    return redirect(url_for('index.index'))  # Redirect back to index if no user_id is provided