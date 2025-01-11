from flask import Blueprint, jsonify, render_template, flash, redirect, url_for
from flask_login import current_user
from .models.cartitem import CartItem
from .models.product import Product
from .models.review import Review

from flask import request, redirect, url_for

bp = Blueprint('coupon', __name__)
