#!/usr/bin/python3
""" Blueprint module """
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_limiter import Limiter
from models import storage
from .blueprints.views import views
from .blueprints.auth import auth, Manager
from .blueprints.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Manager.init_app(app)
    Manager.login_view = 'auth.login'
    CORS(app)
    Session(app)
    Limiter(app, default_limits=["200 per day", "50 per hour"])
    app.register_blueprint(views)
    app.register_blueprint(auth)

    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    @app.teardown_appcontext
    def teardown_db(exception):
        storage.close()

    return app
