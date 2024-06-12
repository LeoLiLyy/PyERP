from flask import Flask, request, session, g, redirect, url_for
import secrets
import logging
from datetime import date
import colorlog
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.translations import load_translations
import os

# Initialize global variables
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    global email
    user = ''
    is_admin = False
    log_name = date.today()
    log_f_name = str(log_name) + '.log'
    users_online = []

    app = Flask(__name__)
    app.secret_key = secrets.token_hex()

    # Logging configuration
    debug = True

    logger = colorlog.getLogger('logger')
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    handler = logging.FileHandler(f'./logs/{log_f_name}')
    handler.setLevel(logging.DEBUG if debug else logging.INFO)

    console = colorlog.StreamHandler()
    console.setLevel(logging.DEBUG if debug else logging.INFO)

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'black',
            'ERROR': 'red',
            'CRITICAL': 'purple'
        }
    )

    handler.setFormatter(formatter)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.debug(f'[!] Logger starting, log saved at: {log_f_name}')
    logger.addHandler(handler)

    # App configuration
    app.config['UPLOAD_FOLDER'] = './uploads'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:toor@db/pyerp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import blueprints
    from app.auth.route import auth_bp
    from app.core.route import core_bp
    from app.inventory.route import inventory_bp
    from app.pro.route import product_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(core_bp, url_prefix='/core')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(product_bp, url_prefix='/pro')

    # Ensure _ is available in templates
    @app.context_processor
    def inject_translations():
        return dict(_=g.translations.get)

    # Define language selector function
    @app.before_request
    def set_language():
        if 'language' not in session:
            session['language'] = request.accept_languages.best_match(['en_US', 'zh_CN'])
        g.translations = load_translations(session['language'])

    @app.route('/set_language', methods=['POST'], endpoint='set_language')
    def set_language_route():
        language = request.form['language']
        session['language'] = language
        return redirect(request.referrer)

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import Employee  # Import here to avoid circular import
    return Employee.query.get(int(user_id))