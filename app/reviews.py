from flask import current_app as app
from flask import render_template, request, redirect, url_for
from flask_login import current_user
from flask import jsonify
import datetime
import csv
import os
 
from .models.review import Review
from .models.user import User

from flask import Blueprint 
bp = Blueprint('reviews', __name__)


# @bp.route('/reviews') 
# def review():
#     # get all reviews from current_user:
#     all_reviews = Review.get_all_by_uid(current_user.id)

#     # render the page by adding information to the index.html file
#     return render_template('review.html',
#                            my_reviews=all_reviews)

@bp.route('/reviews', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        user_id = request.form.get('user_id', type=int)
        if user_id:
            all_reviews = Review.get_5recent_reviews_by_uid(user_id)
            print(user_id)
            if not all_reviews:
                # Handle case where no reviews are found
                message = f"No reviews found for user with ID {user_id}."
                return render_template('review.html', my_reviews=[], message=message)
            return render_template('review.html', my_reviews=all_reviews)
    
    # Default case for GET request
    return render_template('review.html', my_reviews=[])

@bp.route('/reviews/<int:user_id>', methods=['GET'])
def get_recent_reviews(user_id):
    # get the top 5 recent reviews for the provided user id
    top5reviews = Review.get_5recent_reviews_by_uid(user_id)

    # render the page by adding information to the index.html file
    return render_template('review.html',
                           top_reviews=top5reviews)

@bp.route('/write_review/<int:product_id>', methods=['GET', 'POST'])
def write_review(product_id):
    # Logic to handle the review submission
    # Render the review form template, passing in product_id if needed
    return render_template('writeReview.html', product_id=product_id)

@bp.route('/submit_review/<int:product_id>', methods=['POST'])
def submit_review(product_id):
    # Extract data from the form
    rating = request.form.get('rating')
    review_text = request.form.get('review_text')

    # Write this new review to the CSV file
    review_id = Review.count_total_reviews()
    user_id = current_user.id
    print("ID: " + str(current_user.id) + " Name: " + str(current_user.firstname))
    # csv_file_path = '../db/data/Reviews.csv'
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'data', 'Reviews.csv')
    time_created = datetime.datetime.now()
    time_modified = time_created
    num_upvotes = 0

    with open(csv_file_path, mode='a', newline='') as csv_file:
        # csv_file.write("\n")
        writer = csv.writer(csv_file)
        writer.writerow([review_id, user_id, product_id, rating, review_text, time_created, time_modified, num_upvotes])

    # Write to the database
    app.db.execute('''
    INSERT INTO Reviews (id, user_id, product_id, rating, description, time_created, time_modified, num_upvotes)
    VALUES (:review_id, :user_id, :product_id, :rating, :review_text, :time_created, :time_modified, :num_upvotes)
    ''',
    review_id=review_id,
    user_id=user_id,
    product_id=product_id,
    rating=rating,
    review_text=review_text,
    time_created=time_created,
    time_modified=time_modified,
    num_upvotes=0)

    # Logic to save the review, e.g., store it in the database
    return redirect(url_for('index.index'))  # Redirect back to the landing page or a success page
