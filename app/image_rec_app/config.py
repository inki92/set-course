""" Module to store environment configs """

import os


class Config(object):
    """Parent class for environment configs"""
    ENV = os.environ["ENV"] if "ENV" in os.environ else "DEVELOPMENT"
    CSRF_ENABLED = True
    SECRET_KEY = "this_is_a_secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """ Development environment config """
    DEBUG = True


class TestingConfig(Config):
    """ Testing environment config """
    DEBUG = False
