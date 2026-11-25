import os

from flask import Flask, jsonify, redirect, request, session

# Load environment variables from .env files
import dotenv
dotenv.load_dotenv(dotenv_path='.env.secrets')
dotenv.load_dotenv(dotenv_path='.env')

# Load Flask blueprints
from frontend import frontend  # Import the frontend module to register routes
from atproto_bff import atproto_bff  # Import the atproto_bff module to register routes

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

app.config.update(
    SESSION_COOKIE_SECURE=True,      # Only send cookie over HTTPS
    SESSION_COOKIE_HTTPONLY=True,    # Prevent JavaScript (XSS) from reading the cookie
    SESSION_COOKIE_SAMESITE='Lax',   # Protect against CSRF attacks while allowing OAuth redirects
)

# Register the frontend blueprint with the Flask app
app.register_blueprint(frontend)
app.register_blueprint(atproto_bff)


print(f"Server initialised successfully.")

# Run the Flask app if this script is executed directly
# In production you would typically use a WSGI server like Gunicorn or uWSGI to run the app.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)