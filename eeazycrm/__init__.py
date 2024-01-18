from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import inspect
from dotenv import load_dotenv
from flask_mail import Mail
from eeazycrm import config

import os

mail = Mail()

sid = config.TWILIO_ACCOUNT_SID
token=config.WILIO_AUTTH_TOKEN
phone=config.TWILIO_PHONE_NUMBER

from .config import DevelopmentConfig, TestConfig, ProductionConfig

# database handle
db = SQLAlchemy(session_options={"autoflush": False})

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

os.environ['FLASK_ENV'] = 'development'
config_class=ProductionConfig

# encryptor handle
bcrypt = Bcrypt()

# manage user login
login_manager = LoginManager()

# function name of the login route that
# tells the path which facilitates authentication
login_manager.login_view = 'users.login'

# client = Client(sid,token)
def run_install(app_ctx):
    from eeazycrm.install.routes import install
    app_ctx.register_blueprint(install)
    return app_ctx


def create_app(config_class=ProductionConfig):
    app = Flask(__name__, instance_relative_config=True)
    print(app)

    if os.getenv('FLASK_ENV') == 'development':
        config_class = DevelopmentConfig()
    elif os.getenv('FLASK_ENV') == 'production':
        config_class = ProductionConfig()
    elif os.getenv('FLASK_ENV') == 'testing':
        config_class = TestConfig()

    app.config.from_object(config_class)
    app.url_map.strict_slashes = False
    app.jinja_env.globals.update(zip=zip)
    app.config['MAIL_SERVER'] = config.MAIL_SERVER
    app.config['MAIL_PORT'] = config.MAIL_PORT
    app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER


    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app=app)
    login_manager.init_app(app)

    with app.app_context():

       # Obtenez l'objet inspecteur pour le moteur
        inspector = inspect(db.get_engine(app, bind='eeazycrm'))

        # Vérifiez si la table 'app_config' existe
        if 'app_config' not in inspector.get_table_names():
            return run_install(app)
        else:
            from eeazycrm.settings.models import AppConfig
            row = AppConfig.query.first()
            if not row:
                return run_install(app)

        # application is installed so extends the config
        from eeazycrm.settings.models import AppConfig, Currency, TimeZone
        app_cfg = AppConfig.query.first()
        app.config['def_currency'] = Currency.get_currency_by_id(app_cfg.default_currency)
        app.config['def_tz'] = TimeZone.get_tz_by_id(app_cfg.default_timezone)

        # include the routes
        # from eeazycrm import routes
        from eeazycrm.main.routes import main
        from eeazycrm.users.routes import users
 
        from eeazycrm.accounts.routes import accounts
        from eeazycrm.contacts.routes import contacts
        from eeazycrm.settings.routes import settings
        from eeazycrm.settings.app_routes import app_config

        # register routes with blueprint
        app.register_blueprint(main)
        app.register_blueprint(users)
        app.register_blueprint(settings)
        app.register_blueprint(app_config)
        app.register_blueprint(accounts)
        app.register_blueprint(contacts)
        return app


