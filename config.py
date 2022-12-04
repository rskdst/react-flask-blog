import os
class BaseConfig:
    SECRET_KEY = b'_5#y2jL"F4Q8lz\n\xec]flask_app/'
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:950824@localhost:3306/blog'
    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_POOL_TIMEOUT = 30            # 30s
    SQLALCHEMY_POOL_RECYCLE = 60 * 60       # 1 hour
    SQLALCHEMY_ECHO = False

    # celery配置
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    # jwt配置
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'jwt-xxx'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 3600
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(DevelopmentConfig):
    pass


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/blog'
    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_POOL_TIMEOUT = 30            # 30s
    SQLALCHEMY_POOL_RECYCLE = 60 * 60       # 1 hour
    SQLALCHEMY_ECHO = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,

}
