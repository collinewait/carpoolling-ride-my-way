"""
This module sets up the flask emvironment
"""
import sys
import os

from flask import Flask
from flask_cors import CORS
from api.handler import ErrorHandler
from api.config import ENVIRONMENT, TESTING
from api.urls import Urls

APP = Flask(__name__)
APP.testing = TESTING
APP.env = ENVIRONMENT
APP.errorhandler(404)(ErrorHandler.url_not_found)

Urls.generate_url(APP)

CORS(APP)
