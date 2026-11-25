from flask import Flask, jsonify, redirect, request, session, Blueprint
from markupsafe import escape
# from __main__ import app

# Create a flask blueprint for the frontend routes
frontend = Blueprint('frontend', __name__)

@frontend.get('/')
def index():
    did = session.get('did')
    if not did:
        return("<html><body><h1>Pieces</h1><form method='POST' action='/login'><input name='handle' placeholder='Enter your handle'><button type='submit'>Login</button></form></body></html>")
    else:
        return (
        f"<html><body><h1>Pieces</h1><p>Logged in as {escape(did)}</p>"
        "<form method='POST' action='/post'>"
        "<textarea name='text' maxlength='300' required></textarea>"
        "<button type='submit'>Post</button></form>"
        "<form method='POST' action='/logout'><button type='submit'>Log out</button></form>"
        "</body></html>"
    )