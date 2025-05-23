import os
import html
import re
from flask import Flask, request, render_template
from pathlib import Path
import vertexai
from vertexai.generative_models import GenerativeModel
import google.auth
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
import markdown2

# Load environment
load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('KEYFILE_PATH')
credentials, project = google.auth.default()

# Vertex AI init
vertexai.init(project=os.getenv('PROJECT_NAME'), location=os.getenv('LOCATION'), credentials=credentials)
multimodal_model = GenerativeModel(os.getenv("GENMIN_MODEL"))

# Safety config
safety_config = {
    vertexai.generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: vertexai.generative_models.HarmBlockThreshold.BLOCK_NONE,
    vertexai.generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: vertexai.generative_models.HarmBlockThreshold.BLOCK_NONE,
    vertexai.generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: vertexai.generative_models.HarmBlockThreshold.BLOCK_NONE,
    vertexai.generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: vertexai.generative_models.HarmBlockThreshold.BLOCK_NONE,
}

app = Flask(__name__, template_folder='/apps/abcd/sangram/code/templates')

def summarize_code(code, prompt):
    max_chunk_size = 15000
    if len(code) > max_chunk_size:
        chunks = split_code_into_chunks(code, max_chunk_size)
        summaries = []
        for chunk in chunks:
            previous_summary = None
            summaries.append(summarize_chunk(chunk, prompt, previous_summary))
        return ''.join(summaries)
    else:
        return summarize_chunk(code, prompt, None)

def split_code_into_chunks(code, max_chunk_size):
    text_splitter = CharacterTextSplitter(chunk_size=max_chunk_size, chunk_overlap=200)
    chunks = text_splitter.split_text(code)
    return chunks

def summarize_chunk(chunk, prompt, previous_summary):
    chunk = html.escape(chunk)
    full_prompt = prompt.format(chunk)
    response = multimodal_model.generate_content([full_prompt], safety_settings=safety_config)
    return response.text

@app.route('/', methods=['GET', 'POST'])
def chat():
    response_html = None
    if request.method == 'POST':
        user_input = request.form['prompt']
        response_text = summarize_code('', user_input)
        response_html = markdown2.markdown(response_text, extras=["fenced-code-blocks", "code-friendly", "tables"])
    return render_template('ai_assistant.html', response=response_html)

if __name__ == "__main__":
    host = "abcd.dg.dr.com"
    port = 6001
    app.run(debug=True, host=host, port=port)
