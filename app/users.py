from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.review import Review


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



@bp.route('/user/<int:user_id>', methods=['GET'])

def public_view(user_id):
    #user_id = request.args.get('user_id', type=int)
    
    user = User.get(user_id)
    if not user:
        abort(404)  # User not found

    is_seller = user.is_seller if hasattr(user, 'is_seller') else False
    reviews = Review.get_reviews_by_seller_id(user_id) if is_seller else []

    return render_template('public_view.html', user=user, is_seller=is_seller, reviews=reviews)


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

@bp.route('/user/<int:id>')
def product(id):
    user = User.get(id)
    if user:
        return render_template('public_view.html', user=user)
    else:
        return render_template('public_view.html', user=None)

#add profile route
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.update_profile(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            address=form.address.data,
            password=form.password.data if form.password.data else None
        )
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.address.data = current_user.address
    return render_template('profile.html', title='Profile', form=form)