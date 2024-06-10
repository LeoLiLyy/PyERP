from flask import Flask, request, redirect, url_for, session, g
import secrets
import logging
from datetime import date
import colorlog
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.translations import load_translations
from app.models import Employee

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:toor@localhost:8889/pyerp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import blueprints and models
    from app.auth.route import auth_bp
    from app.core.route import core_bp
    from app.models import Employee

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(core_bp, url_prefix='/core')

    # Define language selector function
    @app.before_request
    def set_language():
        if 'language' not in session:
            session['language'] = request.accept_languages.best_match(['en_US', 'zh_CN'])
        g.translations = load_translations(session['language'])

    @app.route('/set_language', methods=['POST'])
    def set_language():
        language = request.form['language']
        session['language'] = language
        return redirect(request.referrer)

    return app


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))