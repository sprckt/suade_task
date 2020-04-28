import os
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    """
    Base Config object
    """

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):

    # Production config

    DEBUG = False


class DevelopmentConfig(Config):

    """
    Dev config
    """

    DEVELOPMENT = True
    DEBUG = True
