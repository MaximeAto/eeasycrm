from .config_vars  import * 



class Config(object):
    DEBUG = False
    TESTING = False
    RBAC_USE_WHITE = True
    PYTHON_VER_MIN_REQUIRED = '3.5.0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = DEV_SECRET_KEY
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DEV_DB_USER}:{DEV_DB_PASS}@{DEV_DB_HOST}/{DEV_DB_NAME}'
    SQLALCHEMY_BINDS = {'eeazycrm': SQLALCHEMY_DATABASE_URI}


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = TEST_SECRET_KEY
    SQLALCHEMY_DATABASE_URI = f'postgresql://{TEST_DB_USER}{TEST_DB_PASS}:@{TEST_DB_HOST}/{TEST_DB_NAME}'


class ProductionConfig(Config):
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_USER}@{DB_HOST}/{DB_NAME}'



#config email
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'melainenkeng@gmail.com'
MAIL_PASSWORD = 'vbpd ofhv muxm vhff'
MAIL_DEFAULT_SENDER = 'melainenkeng@gmail.com' 

#twilio
# TWILIO_ACCOUNT_SID = 'AC536d584dec066c64c3146b4722b55867'
# TWILIO_AUTH_TOKEN = 'f99ba6a35a4fb57c0c76439ef0ef0719'
# TWILIO_PHONE_NUMBER = '+12054794650'

#sms config
TWILIO_ACCOUNT_SID='AC2684bea000f1b584e593c69ddb595e0b'
WILIO_AUTTH_TOKEN='25d7847207792e30c61d5ae0317746bd'
TWILIO_PHONE_NUMBER='+12059740669'

