import time
import json
import jwt
import requests

class GoogleAuthTokenGenerator:
    def __init__(self, keyfile_json_path):
        self.keyfile_json_path = keyfile_json_path
        self.token_cache = None

    def generate_google_auth_token(self):
        try:
            now = int(time.time())
            # Return cached token if valid
            if self.token_cache and self.token_cache['expiresAt'] > now:
                return self.token_cache['token']

            # Read service account keyfile
            with open(self.keyfile_json_path, 'r') as f:
                keyfile = json.load(f)

            client_email = keyfile['client_email']
            private_key = keyfile['private_key']

            # Create JWT
            jwt_payload = {
                'iss': client_email,
                'scope': 'https://www.googleapis.com/auth/cloud-platform',
                'aud': 'https://oauth2.googleapis.com/token',
                'iat': now,
                'exp': now + 3600
            }

            signed_jwt = jwt.encode(jwt_payload, private_key, algorithm='RS256')

            # Exchange JWT for access token
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            body = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                'assertion': signed_jwt
            }

            response = requests.post("https://oauth2.googleapis.com/token", data=body, headers=headers)

            if not response.ok:
                raise Exception(f"Failed to get access token: {response.status_code} {response.text}")

            token_data = response.json()
            token = token_data['access_token']
            expires_in = token_data['expires_in']

            # Cache token
            self.token_cache = {
                'token': token,
                'expiresAt': now + expires_in - 60  # 1 min buffer
            }

            return token

        except Exception as e:
            print(f"Failed to generate Google Auth token: {str(e)}")
            raise
