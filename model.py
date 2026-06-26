from flask import Flask, render_template, request
from pypdf import PdfReader
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    question = request.form.get('question')
    model = request.form.get('model', 'tinyllama')
    pdf_file = request.files.get('pdf_file')
    
    if not question:
        return "Error: Enter a question"
    pdf_reader = PdfReader(pdf_file)
    pdf_text = ""
    
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    
    # Combine PDF text with question
    prompt = f"PDF Content:\n{pdf_text}\n\nQuestion: {question}"
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60
        )
        output = response.json().get("response", "No response")
        return output
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)