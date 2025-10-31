import os
import logging

from flask import Flask
# from sqlalchemy.orm import DeclarativeBase

# import models  # noqa: F401

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# create the app
app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.secret_key = os.environ.get("SESSION_SECRET")

from routes import *