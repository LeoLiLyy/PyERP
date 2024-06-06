from flask import Flask
import os
from flask_login import LoginManager
from .auth import auth_bp


# from .inventory import inventory_bp
# from .user import user_bp


def create_app():
    # don't modify the code below if you are not an idiot and wants the code to run
    global email, login_manager
    user = ''
    is_admin = False
    log_name = date.today()
    log_f_name = str(log_name) + '.log'
    users_online = []
    db = SQLAlchemy(app, session_options={"expire_on_commit": False})

    # logging config

    debug = True

    logger = colorlog.getLogger('logger')
    if debug == True:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    handler = logging.FileHandler('./logs/' + str(log_f_name))
    if debug == True:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)
    console = colorlog.StreamHandler()
    if debug == True:
        console.setLevel(logging.DEBUG)
    else:
        console.setLevel(logging.INFO)
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)-8s%(reset)s   | %(log_color)s%(message)s%(reset)s",
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
    time.sleep(1)
    logger.debug('[!] Logger starting, log saved at : ' + str(log_f_name))
    logger.addHandler(handler)

    # Cryptocurrency Token config
    # mint = Pubkey.from_string(
    #     "<token_address>")  # eg: https://solscan.io/token/FpekncBMe3Vsi1LMkh6zbNq8pdM6xEbNiFsJBRcPbMDQ**
    # program_id = Pubkey.from_string(
    #     "<program_id>")  # eg: https://solscan.io/account/**TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA**
    #
    # privkey = '<wallet_private_key>'
    # key_pair = Keypair.from_base58_string(privkey)
    #
    # solana_client = Client("https://api.mainnet-beta.solana.com")
    # spl_client = Token(conn=solana_client, pubkey=mint, program_id=program_id, payer=key_pair)

    # source = Pubkey.from_string('<wallet_address>')
    # dest = Pubkey.from_string('<wallet_address>')

    # file_path = Path('./uploads/')
    #
    # with FTP('server.address.com', 'USER', 'PWD') as ftp, open(file_path, 'rb') as file:
    #     ftp.storbinary(f'STOR {file_path.name}', file)

    app.config.from_object(config_class)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(inventory_bp, url_prefix='/inventory')
    # app.register_blueprint(user_bp, url_prefix='/user')
    app.config['SECRET_KEY'] = str(secrets.token_hex())
    UPLOAD_FOLDER = './uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:toor@db/pyerp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))
