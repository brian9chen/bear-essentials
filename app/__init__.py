from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB

# Create LoginManager instance but don't initialize it yet
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    
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

    from .purchases import bp as purchases_bp
    app.register_blueprint(purchases_bp)

    return app