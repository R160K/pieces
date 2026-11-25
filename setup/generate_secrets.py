#!/usr/bin/env python3

import json, secrets
from atproto_crypto.jwk import generate_p256_jwk

print("This script will generate a secret for Flask and a JWK for OAuth.")

FLASK_SECRET_KEY = secrets.token_urlsafe(32)
# TODO: Additional keys need unique kid values.
OAUTH_PRIVATE_JWK = json.dumps(generate_p256_jwk(kid="key-1"))

with open(".env.secrets", "w") as f:
    f.write(f"FLASK_SECRET_KEY='{FLASK_SECRET_KEY}'\n")
    f.write(f"OAUTH_PRIVATE_JWK='{OAUTH_PRIVATE_JWK}'\n")

print("Secrets generated and saved to .env.secrets.")                               