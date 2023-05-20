from flask import Flask, render_template, request, redirect, url_for
from summarize_link import get_text_from_url, get_summary
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# Read the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        text = get_text_from_url(url)
        summaries = get_summary(text, api_key)
        return render_template('summary.html', summaries=summaries)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)