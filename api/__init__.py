"""
This module sets up the flask emvironment
"""
import sys
import os

from flask import Flask
from flask_cors import CORS
from api.handler import ErrorHandler
from api.config import ENVIRONMENT, TESTING, SECRET_KEY, DEBUG
from api.urls import Urls
from api.models.database_connection import DatabaseAccess

APP = Flask(__name__)
APP.secret_key = SECRET_KEY
APP.testing = TESTING
APP.debug = DEBUG
APP.env = ENVIRONMENT
APP.errorhandler(404)(ErrorHandler.url_not_found)

Urls.generate_url(APP)
DatabaseAccess.create_tables(APP)

CORS(APP)
