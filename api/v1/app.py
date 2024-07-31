#!/usr/bin/python3
""" Flask Application """
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from models import storage
from api.v1.views import app_views
from api.v1.email import mail  # Import the mail instance
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER', 'smtp.example.com')
app.config['MAIL_PORT'] = environ.get('MAIL_PORT', 587)
app.config['MAIL_USE_TLS'] = environ.get('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER')

# Initialize Flask-Mail
mail.init_app(app)

app.register_blueprint(app_views)
# cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


app.config['SWAGGER'] = {
    'title': 'IMS Restful API Documentation',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('IMS_API_HOST', '0.0.0.0')
    port = environ.get('IMS_API_PORT', '5000')

    app.run(host=host, port=port, threaded=True, debug=True)
