"""Single-operator authentication; deployment must terminate HTTPS."""
import base64
import hashlib
import hmac
import ipaddress
import os
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

COOKIE = 'researchingos_session'
SAFE = {'GET', 'HEAD', 'OPTIONS'}


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
    signature = hmac.new(password.encode(), ('session:' + expiry).encode(), hashlib.sha256).hexdigest()
    return expiry + '.' + signature


def valid_session(value, password):
    try:
        expiry, signature = value.split('.', 1)
        expected = hmac.new(password.encode(), ('session:' + expiry).encode(), hashlib.sha256).hexdigest()
        return int(expiry) > time.time() and hmac.compare_digest(signature, expected)
    except (ValueError, AttributeError):
        return False


class OperatorAccess(BaseHTTPMiddleware):
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
        cookie_ok = valid_session(request.cookies.get(COOKIE), password)
        # Browser mutations require an allowlisted Origin, including session creation.
        if request.method not in SAFE and not basic_ok and (not origin or not cookie_ok):
            return JSONResponse({'detail': 'Authentication and allowed Origin required'}, status_code=401)
        if not basic_ok and not cookie_ok:
            return JSONResponse({'detail': 'Authentication required'}, status_code=401)
        response = await call_next(request)
        if request.url.path == '/api/session' and request.method == 'POST' and basic_ok:
            response.set_cookie(COOKIE, session_value(password), max_age=8 * 3600,
                                httponly=True, secure=os.getenv('RESEARCHINGOS_COOKIE_SECURE', 'true') == 'true',
                                samesite='strict', path='/')
        if request.url.path.startswith('/vault/'):
            response.headers['Content-Security-Policy'] = "sandbox; default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:;"
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
