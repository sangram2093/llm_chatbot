import os
from google.auth.credentials import Credentials
import vertexai
from vertexai.generative_models import GenerativeModel

# Load environment variables
os.environ["WIF_TOKEN_PATH"] = "/path/to/your/wif_token.txt"  # Update this
os.environ["PROJECT_NAME"] = "your-gcp-project-id"
os.environ["LOCATION"] = "us-central1"
os.environ["GENMIN_MODEL"] = "gemini-pro"

# Step 1: Load token from file
with open(os.environ["WIF_TOKEN_PATH"], "r") as file:
    token = file.read().strip()

# Step 2: Create Credentials object from token
credentials = Credentials(token=token)

# Step 3: Initialize Vertex AI with the credentials
vertexai.init(
    project=os.environ["PROJECT_NAME"],
    location=os.environ["LOCATION"],
    credentials=credentials
)

# Step 4: Create Gemini model and send prompt
model = GenerativeModel(os.environ["GENMIN_MODEL"])
response = model.generate_content("Write a short poem about the moon.")

# Step 5: Print the response
print(response.text)
