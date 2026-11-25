# TODO: Add option to redirect to a specific page after login/logout, instead of always redirecting to the home page.

import json
import os
import secrets

from atproto import Client, OAuthClient, models
from atproto.exceptions import OAuthCallbackError
from flask import jsonify, redirect, request, session, Blueprint, current_app

from stores import session_store, state_store

HOSTNAME = os.environ.get('HOSTNAME', 'http://localhost:5000')

keys=[json.loads(os.environ['OAUTH_PRIVATE_JWK'])]

oauth_client = OAuthClient.confidential(
    client_id=f'{HOSTNAME}/oauth-client-metadata.json',
    redirect_uri=f'{HOSTNAME}/oauth/callback',
    scope=f'atproto repo:{models.ids.AppBskyFeedPost}?action=create',
    keys=[json.loads(os.environ['OAUTH_PRIVATE_JWK'])],
    metadata={'client_name': 'Pieces', 'jwks_uri': f'{HOSTNAME}/oauth/jwks.json'},
    state_store=state_store,  # your database, see "Storing sessions"
    session_store=session_store,
)

atproto_bff = Blueprint('atproto_bff', __name__)

@atproto_bff.get('/oauth-client-metadata.json')
def client_metadata():
    return jsonify(oauth_client.client_metadata)


@atproto_bff.get('/oauth/jwks.json')
def jwks():
    return jsonify(oauth_client.jwks)




@atproto_bff.post('/login')
def login():
    session['oauth_state'] = secrets.token_urlsafe()
    return redirect(oauth_client.authorize(request.form['handle'], state=session['oauth_state']))

@atproto_bff.post('/logout')
def logout():
    did = session.get('did')
    if did:
        try:
            # Restores and revokes ONLY this browser's <did>:<sid> session
            oauth_client.restore(did).revoke()
        except Exception:
            current_app.logger.exception('Failed to revoke OAuth session on logout')
    session.pop('did', None)
    session.pop('sid', None)
    return redirect('/')




@atproto_bff.get('/oauth/callback')
def callback():
    # Generate a unique browser session ID before callback() saves to session_store
    session['sid'] = secrets.token_urlsafe(16)

    try:
        result = oauth_client.callback(request.args.to_dict())
    except OAuthCallbackError:
        session.pop('sid', None)
        return 'Login failed 1', 400

    expected_state = session.pop('oauth_state', None)
    if not expected_state or not result.state or not secrets.compare_digest(result.state, expected_state):
        result.session.revoke()
        session.pop('sid', None)
        return 'Login failed 2', 400

    session['did'] = result.session.did
    return redirect('/')


@atproto_bff.post('/post')
# def post():
#     client = Client()
#     client.login_oauth(oauth_client.restore(session['did']))
#     client.send_post(request.form['text'])
#     return redirect('/')
def post():
    did = session.get('did')
    if not did:
        return redirect('/')
    text = request.form.get('text', '').strip()
    if not text:
        return 'Empty post', 400
    try:
        client = Client()
        client.login_oauth(oauth_client.restore(did))
        client.send_post(text)
    except Exception:
        current_app.logger.exception('Post failed')
        session.pop('did', None)
        return 'Session expired, please log in again', 401
    return redirect('/')