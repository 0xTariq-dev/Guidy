#!/usr/bin/python3
""" Blueprint module """
from flask import Flask, Blueprint
from flask_cors import CORS
from app_server.blueprints.config import Config
# from app_server.blueprints.auth import auth
from app_server.blueprints.views import views

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    from .blueprints.views import views
    app.register_blueprint(views)

    return app    
    
    