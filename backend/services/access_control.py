"""Single-operator authentication; deployment must terminate HTTPS."""
import base64
import hashlib
import hmac
import ipaddress
import os
import secrets
import threading
import time
from collections import deque
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

COOKIE = 'researchingos_session'
SAFE = {'GET', 'HEAD', 'OPTIONS'}
# Optional legacy executors have not passed the bounded-worker release contract.
# Keep local research experimentation available; public authenticated deployment
# exposes the qualified durable pipeline instead of silently launching these.
LOCAL_EXECUTORS = {'/api/feynman/autoresearch', '/api/fx/dispatch', '/api/fx/mcp/call',
                   '/api/voice/synthesize', '/api/ecc/sync', '/api/evomap/pilot'}


def origins():
    return [x.strip().rstrip('/') for x in os.getenv('RESEARCHINGOS_ORIGINS', 'http://127.0.0.1:3000,http://localhost:3000').split(',') if x.strip()]


def credentials():
    return os.getenv('RESEARCHINGOS_OPERATOR', 'operator'), os.getenv('RESEARCHINGOS_PASSWORD', '')


def validate_configuration():
    mode = os.getenv('RESEARCHINGOS_ACCESS_MODE', 'authenticated')
    if mode == 'local':
        return
    if mode != 'authenticated' or len(credentials()[1]) < 32:
        raise RuntimeError('Configure operator authentication before starting workers')
    if not origins() or any(not origin.startswith('https://') or '*' in origin for origin in origins()):
        raise RuntimeError('Authenticated deployment requires explicit HTTPS origins')
    if os.getenv('RESEARCHINGOS_COOKIE_SECURE', 'true') != 'true':
        raise RuntimeError('Authenticated deployment requires secure session cookies')
    hosts = os.getenv('RESEARCHINGOS_HOSTS', 'localhost,127.0.0.1,[::1]')
    if '*' in hosts or not hosts.strip():
        raise RuntimeError('Configure explicit trusted hosts')


def session_value(password):
    expiry = str(int(time.time()) + 8 * 3600)
    nonce = secrets.token_hex(24)
    message = expiry + '.' + nonce
    signature = hmac.new(password.encode(), ('session:' + message).encode(), hashlib.sha256).hexdigest()
    return message + '.' + signature


def valid_session(value, password):
    try:
        expiry, nonce, signature = value.split('.')
        expected = hmac.new(password.encode(), ('session:' + expiry + '.' + nonce).encode(), hashlib.sha256).hexdigest()
        return int(expiry) > time.time() and hmac.compare_digest(signature, expected)
    except (ValueError, AttributeError):
        return False


class OperatorAccess(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Single-process deployment: no unbounded per-IP map and no forwarded-IP
        # trust. All failed credential paths share this rolling admission window.
        self.failures = deque(maxlen=10)
        self.sessions = {}
        self.guard = threading.Lock()

    def failed_attempt(self):
        with self.guard:
            now = time.monotonic()
            while self.failures and self.failures[0] <= now - 60:
                self.failures.popleft()
            if len(self.failures) >= 10:
                return False
            self.failures.append(now)
            return True

    def active_session(self, value, password):
        if not valid_session(value, password):
            return False
        with self.guard:
            return self.sessions.get(hashlib.sha256(value.encode()).hexdigest(), 0) > time.time()

    def issue_session(self, password):
        value = session_value(password)
        with self.guard:
            now = time.time()
            self.sessions = {key: expiry for key, expiry in self.sessions.items() if expiry > now}
            # Bound memory even if the operator repeatedly signs in. Evict oldest.
            if len(self.sessions) >= 128:
                self.sessions.pop(next(iter(self.sessions)))
            self.sessions[hashlib.sha256(value.encode()).hexdigest()] = int(value.split('.')[0])
        return value

    async def dispatch(self, request: Request, call_next):
        mode = os.getenv('RESEARCHINGOS_ACCESS_MODE', 'authenticated')
        origin = request.headers.get('origin')
        if origin and origin.rstrip('/') not in origins():
            return JSONResponse({'detail': 'Origin not allowed'}, status_code=403)
        if mode == 'local':
            try:
                local = ipaddress.ip_address(request.client.host).is_loopback
            except (ValueError, AttributeError):
                local = False
            # No forwarded-header trust: local mode is never a reverse-proxy deployment mode.
            host = request.url.hostname
            if not local or host not in {'localhost', '127.0.0.1', '::1'}:
                return JSONResponse({'detail': 'Local mode requires loopback access'}, status_code=403)
            return await call_next(request)
        username, password = credentials()
        if mode != 'authenticated' or len(password) < 32:
            return JSONResponse({'detail': 'Operator access is not configured'}, status_code=503)
        basic_ok = False
        authorization = request.headers.get('authorization', '')
        if authorization.startswith('Basic '):
            try:
                user, supplied = base64.b64decode(authorization[6:], validate=True).decode().split(':', 1)
                basic_ok = hmac.compare_digest(user.encode(), username.encode()) and hmac.compare_digest(supplied.encode(), password.encode())
            except (ValueError, UnicodeError):
                pass
        cookie = request.cookies.get(COOKIE)
        cookie_ok = self.active_session(cookie, password)
        if not basic_ok and not cookie_ok and not self.failed_attempt():
            return JSONResponse({'detail': 'Too many failed authentication attempts'}, status_code=429,
                                headers={'Retry-After': '60', 'Cache-Control': 'no-store'})
        # Browser mutations require an allowlisted Origin, including session creation.
        if request.method not in SAFE and not basic_ok and (not origin or not cookie_ok):
            return JSONResponse({'detail': 'Authentication and allowed Origin required'}, status_code=401)
        if not basic_ok and not cookie_ok:
            return JSONResponse({'detail': 'Authentication required'}, status_code=401)
        if request.method not in SAFE and request.url.path.rstrip('/') in LOCAL_EXECUTORS:
            return JSONResponse({'detail': 'This experimental executor is available only in loopback local mode; use the durable research workflow in deployment'},
                                status_code=403)
        response = await call_next(request)
        if request.url.path == '/api/session' and request.method == 'DELETE':
            with self.guard:
                if cookie:
                    self.sessions.pop(hashlib.sha256(cookie.encode()).hexdigest(), None)
            response.delete_cookie(COOKIE, path='/', secure=True, httponly=True, samesite='strict')
        elif request.url.path == '/api/session' and request.method == 'POST' and basic_ok:
            response.set_cookie(COOKIE, self.issue_session(password), max_age=8 * 3600,
                                httponly=True, secure=os.getenv('RESEARCHINGOS_COOKIE_SECURE', 'true') == 'true',
                                samesite='strict', path='/')
        if request.url.path.startswith('/vault/'):
            response.headers['Content-Security-Policy'] = "sandbox; default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:;"
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
