from flask import render_template, request, redirect, url_for
from flask_login import current_user
from flask import jsonify
import datetime
 
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
