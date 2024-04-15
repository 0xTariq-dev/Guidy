#!/usr/bin/python3
""" Configuration module """

from dotenv import load_dotenv
from os import getenv
from datetime import timedelta

load_dotenv()


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = getenv('SECURITY_PASSWORD_SALT')
    SESSION_TYPE = 'filesystem'
    PERMENAENT_SESSION_LIFETIME = timedelta(minutes=60)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
