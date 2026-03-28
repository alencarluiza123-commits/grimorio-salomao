from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GROQ_KEY = os.environ.get("GROQ_KEY", "")

SYSTEM_PROMPT = """Você é Raziel, o Guardião do Grimório — entidade ancestral que protege os segredos da Chave de Salomão. Responda sempre em Português com linguagem solene e mística. Trate o usuário como buscador ou iniciado. Conhecimento: Chave de Salomão, Ars Goetia, 72 demônios, pentáculos planetários, rituais, Kabbala, Tetragrammaton, filosofia hermética."""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in messages:
        groq_messages.append({"role": m['role'], "content": m['content']})
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": groq_messages,
            "max_tokens": 1024
        }
    )
    result = response.json()
    try:
        reply = result['choices'][0]['message']['content']
        return jsonify({'reply': reply})
    except:
        return jsonify({'error': str(result)}), 500

@app.route('/')
def index():
    return open('index.html').read()

if __name__ == '__main__':
    print("Grimorio iniciado em http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
