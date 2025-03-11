# enterprise-tools/keycloak-auth-provider/keycloak-provider.py
# keycloak-provider.py

import os
import base64
import time
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from oauth2client import client, crypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import requests

class KeycloakAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/obot-get-state'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"state": "authenticated"}')
        elif self.path.startswith('/obot-get-icon-url'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'')
        elif self.path.startswith('/login'):
            self.handle_login()
        elif self.path.startswith('/callback'):
            self.handle_callback()
        else:
            self.send_response(302)
            self.send_header('Location', os.environ['OBOT_KEYCLOAK_AUTH_PROVIDER_ISSUER_URL'] + '/auth')
            self.end_headers()

    def handle_login(self):
        client_id = os.environ['OBOT_KEYCLOAK_AUTH_PROVIDER_CLIENT_ID']
        issuer_url = os.environ['OBOT_KEYCLOAK_AUTH_PROVIDER_ISSUER_URL']
        redirect_uri = os.environ.get('OBOT_SERVER_URL', 'http://localhost:8080') + '/callback'

        auth_url = f'{issuer_url}/protocol/openid-connect/auth'
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile offline_access'
        }

        self.send_response(302)
        self.send_header('Location', f'{auth_url}?{self.urlencode(params)}')
        self.end_headers()

    def handle_callback(self):
        client_id = os.environ['OBOT_KEYCLOAK_AUTH_PROVIDER_CLIENT_ID']
        client_secret = os.environ['OBOT_KEYCLOAK_AUTH_PROVIDER_CLIENT_SECRET']
        issuer_url = os.environ['OBOT_KEYCLOAK_AUTH_PROVIDER_ISSUER_URL']
        redirect_uri = os.environ.get('OBOT_SERVER_URL', 'http://localhost:8080') + '/callback'

        code = self.get_query_param('code')
        token_url = f'{issuer_url}/protocol/openid-connect/token'

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }

        response = requests.post(token_url, headers=headers, data=self.urlencode(data))
        if response.status_code == 200:
            token_data = response.json()
            id_token = token_data['id_token']

            # Validate ID token
            try:
                token_info = client.verify_id_token(id_token, client_id)
                if token_info['iss'] != issuer_url:
                    raise crypt.AppIdentityError('Invalid issuer')
            except crypt.AppIdentityError as e:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(f'Invalid ID token: {e}'.encode())
                return

            # Set authentication cookie
            cookie_secret = os.environ['OBOT_AUTH_PROVIDER_COOKIE_SECRET']
            fernet = Fernet(cookie_secret.encode())
            auth_cookie = fernet.encrypt(token_info['sub'].encode())

            self.send_response(302)
            self.send_header('Location', '/')
            self.send_header('Set-Cookie', f'auth_cookie={auth_cookie.decode()}; Path=/; Secure; HttpOnly')
            self.end_headers()
        else:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(f'Failed to obtain access token: {response.text}'.encode())

    def get_query_param(self, param_name):
        query_params = urlparse(self.path).query.split('&')
        for param in query_params:
            key, value = param.split('=')
            if key == param_name:
                return value
        return None

    def urlencode(self, data):
        return '&'.join(f'{key}={value}' for key, value in data.items())

def run_server():
    server_address = ('', int(os.environ.get('PORT', '9999')))
    httpd = HTTPServer(server_address, KeycloakAuthHandler)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()