from flask import Flask
from flask_login import LoginManager
import os
from .config import Config
from .db import DB

# Create LoginManager instance but don't initialize it yet
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
    
    # Initialize login_manager with the app
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'  # Specify the login route

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .cartitem import bp as cartitem_bp
    app.register_blueprint(cartitem_bp)

    from .inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp)  
    
    from .reviews import bp as review_bp
    app.register_blueprint(review_bp)

    from .purchases import bp as purchases_bp
    app.register_blueprint(purchases_bp)

    from .order import bp as order_bp
    app.register_blueprint(order_bp)

    from .seller_fulfillment import bp as fulfillment_bp
    app.register_blueprint(fulfillment_bp)

    from .coupon import bp as coupon_bp
    app.register_blueprint(coupon_bp)

    return app