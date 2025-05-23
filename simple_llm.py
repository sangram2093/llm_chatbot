import os
from google.oauth2.credentials import Credentials
import vertexai
from vertexai.generative_models import GenerativeModel

# Set required environment variables
os.environ["WIF_TOKEN_PATH"] = "/path/to/your/wif_token.txt"
os.environ["PROJECT_NAME"] = "your-gcp-project-id"
os.environ["LOCATION"] = "us-central1"
os.environ["GENMIN_MODEL"] = "gemini-pro"

# Step 1: Load access token from file
with open(os.environ["WIF_TOKEN_PATH"], "r") as file:
    access_token = file.read().strip()

# Step 2: Create Credentials object from access token
credentials = Credentials(
    token=access_token,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Step 3: Initialize Vertex AI with the credentials
vertexai.init(
    project=os.environ["PROJECT_NAME"],
    location=os.environ["LOCATION"],
    credentials=credentials
)

# Step 4: Send a prompt to Gemini
model = GenerativeModel(os.environ["GENMIN_MODEL"])
response = model.generate_content("Write a short poem about the moon.")

# Step 5: Print the result
print(response.text)
