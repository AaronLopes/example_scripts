import os, sys, requests, re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import openai

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = soup.find_all('p')
    text = ""
    for paragraph in paragraphs:
        text += paragraph.get_text()

    return text

def get_summary(text, api_key):
    text = preprocess_text(text)
    openai.api_key = api_key
    tokens_per_chunk = 2046
    max_chunks = len(text) // tokens_per_chunk + (1 if len(text) % tokens_per_chunk > 0 else 0)
    text_chunks = [text[i * tokens_per_chunk:(i + 1) * tokens_per_chunk] for i in range(max_chunks)]

    summaries = []
    for chunk in text_chunks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": f"Please summarize the following text:\n{chunk}\n"},
            ],
            temperature=0.7,
            max_tokens=2046,
        )
        summary = response.choices[0].message['content'].strip()
        print(summary)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarize_link.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    # Load environment variables from the .env file
    load_dotenv()
    # Read the API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key is None:
        print("Error: OPENAI_API_KEY not found in .env file or environment variables.")
        sys.exit(1)

    text = get_text_from_url(url)
    get_summary(text, api_key)
