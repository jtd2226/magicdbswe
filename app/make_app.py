#This file so main can be imported as package
# import models
# import logging
# from flask import current_app, Flask, redirect, url_for

# def create_app(config, debug=False, testing=False, config_overrides=None):
#     app = Flask(__name__)
#     app.config.from_object(config)

#     app.debug = debug
#     app.testing = testing

#     if config_overrides:
#         app.config.update(config_overrides)

#     # Configure logging
#     if not app.testing:
#         logging.basicConfig(level=logging.INFO)

#     # Setup the data model.
#     with app.app_context():
#         models.init_app(app)

#     return app

