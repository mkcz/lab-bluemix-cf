######################################################################
# Copyright 2016, 2022 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and CouchDB database
"""
import sys
import logging
from flask import Flask
from .models import Pet

# Create Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "please, tell nobody... Shhhh"
app.config["LOGGING_LEVEL"] = logging.INFO

# Import the routes After the Flask app is created
# pylint: disable=wrong-import-position, cyclic-import
from service import routes, models, error_handlers

# Set up logging for production
print(f"Setting up logging for {__name__}...")
app.logger.propagate = False
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    # Make all log formats consistent
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", "%Y-%m-%d %H:%M:%S %z"
    )
    for handler in app.logger.handlers:
        handler.setFormatter(formatter)
    app.logger.info("Logging handler established")

app.logger.info(70 * "*")
app.logger.info("  P E T   S T O R E   S E R V I C E  ".center(70, "*"))
app.logger.info(70 * "*")
app.logger.info("Service initialized!")


@app.before_first_request
def init_db(dbname="pets"):
    """Initialize the model"""
    Pet.init_db(dbname)
