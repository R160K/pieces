import json
import redis
from atproto import OAuthSessionData, OAuthStateData
from flask import session

class RedisStore:
    def __init__(self, r, prefix, data_cls, ttl=None, per_browser=False):
        self._r = r
        self._prefix = prefix
        self._cls = data_cls
        self._ttl = ttl
        self._per_browser = per_browser

    def _make_key(self, key):
        if self._per_browser:
            sid = session.get('sid')
            if sid:
                return f'{self._prefix}:{key}:{sid}'
        return f'{self._prefix}:{key}'

    def get(self, key):
        value = self._r.get(self._make_key(key))
        return self._cls.from_dict(json.loads(value)) if value else None

    def set(self, key, value):
        self._r.set(self._make_key(key), json.dumps(value.to_dict()), ex=self._ttl)

    def delete(self, key):
        self._r.delete(self._make_key(key))

r = redis.Redis(host='127.0.0.1', port=6379, db=0)
# Enable per_browser=True on session_store
session_store = RedisStore(r, 'oauth-session', OAuthSessionData, per_browser=True)
state_store = RedisStore(r, 'oauth-state', OAuthStateData, ttl=600)