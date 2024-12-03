from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange

from .models.user import User
from .models.review import Review
from .models.order import Order

from flask import Blueprint, render_template, abort
bp = Blueprint('users', __name__)


#update profile form
class UpdateProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[])
    password2 = PasswordField(
        'Repeat New Password', validators=[EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        if email.data != current_user.email and User.email_exists(email.data):
            raise ValidationError('This email is already in use. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])  # New address field
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

class AddBalanceForm(FlaskForm):
    amount = DecimalField('Amount to Add ($)', validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than $0.")])
    submit_add = SubmitField('Add to Balance')

# Form to Withdraw Balance
class WithdrawBalanceForm(FlaskForm):
    amount = DecimalField('Amount to Withdraw ($)', validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than $0.")])
    submit_withdraw = SubmitField('Withdraw from Balance')



@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Use default values for balance and is_seller
        if User.register(
            uid=User.get_total_users(),  # Generate a new user ID
            email=form.email.data,
            password=form.password.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            address=form.address.data,       # New address field
            balance=0,                       # Default balance
            is_seller=False                  # Default to non-seller
        ):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route('/user/<int:user_id>')
def public_view(user_id):
    user = User.get(user_id)
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of reviews per page
    
    if user:
        reviews = Review.get_sortedByUpvote_by_sellerid(seller_id=user_id)
        
        if current_user.is_authenticated:
            for review in reviews:
                review.user_vote = Review.get_user_vote(current_user.id, review.id)
        else:
            for review in reviews:
                review.user_vote = 0
        
        num_reviews = len(reviews)
        avg_rating = Review.get_avg_rating_by_sellerid(seller_id=user_id)
        
        for review in reviews:
            reviewer = User.get(review.user_id)
            review.user_firstname = reviewer.firstname
            review.user_lastname = reviewer.lastname
        
        # Create pagination
        total_reviews = len(reviews)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_reviews = reviews[start_idx:end_idx]
        
        pagination = {
            'page': page,
            'per_page': per_page,
            'total': total_reviews,
            'pages': (total_reviews + per_page - 1) // per_page,
            'items': paginated_reviews
        }
        
        if current_user.is_authenticated:
            review = Review.has_user_reviewed_seller(current_user.id, user.id)
            has_purchased = User.has_purchased_from_seller(current_user.id, user.id)
            setattr(user, 'has_review', bool(review))
            setattr(user, 'review_id', review[0] if review else None)
            setattr(user, 'has_purchased', has_purchased)
            
        else:
            setattr(user, 'has_review', False)
            setattr(user, 'review_id', None)
            setattr(user, 'has_purchased', False)
        
        return render_template('public_view.html', 
                             user=user, 
                             reviews=paginated_reviews,
                             num_reviews=num_reviews,
                             avg_rating=avg_rating,
                             pagination=pagination,
                             is_seller=user.is_seller)
    else:
        return render_template('public_view.html', user=None)

#add profile route
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    add_balance_form = AddBalanceForm()
    withdraw_balance_form = WithdrawBalanceForm()

    if form.validate_on_submit() and form.submit.data:
        try:
            current_user.update_profile(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                email=form.email.data,
                address=form.address.data,
                password=form.password.data if form.password.data else None
            )
            flash('Your profile has been updated.', 'success')
            return redirect(url_for('users.profile'))
        except Exception as e:
            flash('Failed to update profile. Please try again.', 'danger')


    elif add_balance_form.validate_on_submit() and add_balance_form.submit_add.data:
        try:
            amount = float(add_balance_form.amount.data)
            current_user.add_balance(amount)
            flash(f"Successfully added ${amount:.2f} to your balance.", 'success')
            return redirect(url_for('users.profile'))
        except ValueError as ve:
            flash(str(ve), 'danger')
        except Exception as e:
            flash('Failed to add balance. Please try again.', 'danger')

    elif withdraw_balance_form.validate_on_submit() and withdraw_balance_form.submit_withdraw.data:
        try:
            amount = float(withdraw_balance_form.amount.data)
            current_user.withdraw_balance(amount)
            flash(f"Successfully withdrew ${amount:.2f} from your balance.", 'success')
            return redirect(url_for('users.profile'))
        except ValueError as ve:
            flash(str(ve), 'danger')
        except Exception as e:
            flash('Failed to withdraw balance. Please try again.', 'danger')

    elif request.method == 'GET':
        # Populate the profile form with current user data
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.address.data = current_user.address


    # For reviews table:

    page = request.args.get('page', 1, type=int)
    
    product_reviews = Review.get_all_prodName_by_uid(user_id=current_user.id, page=page, per_page=5)
    total_product_reviews = Review.count_product_reviews_by_uid(current_user.id)
    
    seller_reviews = Review.get_all_sellerName_by_uid(user_id=current_user.id, page=page, per_page=5)
    total_seller_reviews = Review.count_seller_reviews_by_uid(current_user.id)
    
    # Create a simple pagination-like object
    class Pagination:
        def __init__(self, items, page, per_page, total):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = total
            
        @property
        def pages(self):
            return max(1, (self.total + self.per_page - 1) // self.per_page)
            
        @property
        def has_prev(self):
            return self.page > 1
            
        @property
        def has_next(self):
            return self.page < self.pages
            
        @property
        def prev_num(self):
            return self.page - 1
            
        @property
        def next_num(self):
            return self.page + 1
            
        def iter_pages(self):
            for i in range(1, self.pages + 1):
                yield i
    
    # Create pagination object
    my_product_reviews = Pagination(product_reviews, page, per_page=5, total=total_product_reviews)
    my_seller_reviews = Pagination(seller_reviews, page, per_page=5, total=total_seller_reviews)
    
    # get order history if user is a seller
    order_history = []
    if current_user.is_seller:
        order_history = Order.get_all_by_seller(current_user.id)
    
    return render_template(
        'profile.html',
        title='Profile',
        form=form,
        add_balance_form=add_balance_form,
        withdraw_balance_form=withdraw_balance_form,
        balance=current_user.balance,
        my_product_reviews=my_product_reviews,
        my_seller_reviews=my_seller_reviews,
        order_history=order_history
    )