from google_token_generator import GoogleAuthTokenGenerator

generator = GoogleAuthTokenGenerator("path/to/your/keyfile.json")
token = generator.generate_google_auth_token()
print("Access Token:", token)
