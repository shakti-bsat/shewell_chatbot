"""
SheWell — Flask backend
Drop this file into your site_analyser project folder alongside
generator.py, retriever.py, embeddings.py, etc.

Run:
    pip install flask flask-cors
    python app.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

# ── Import your existing modules ──────────────────────────────────────────────
from generator import generate_answer
from retriever import retrieve          # adjust if your function name differs

app = Flask(__name__)
CORS(app)  # allows the HTML frontend (any origin) to call this API


@app.route('/ask', methods=['POST'])
def ask():
    data  = request.get_json(silent=True) or {}
    query = data.get('query', '').strip()

    if not query:
        return jsonify({'error': 'Empty query'}), 400

    # 1. Retrieve relevant context from your vector store / embeddings
    try:
        context = retrieve(query, documents)
    except Exception as e:
        print(f'[retriever] error: {e}')
        context = ''

    # 2. Generate answer via Mistral (through generator.py)
    try:
        answer = generate_answer(query, context)
    except Exception as e:
        print(f'[generator] error: {e}')
        return jsonify({'error': 'Model error', 'detail': str(e)}), 500

    return jsonify({'answer': answer})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'SheWell'})


if __name__ == '__main__':
    print('\n🌿 SheWell backend starting...')
    print('   → http://localhost:5000\n')
    app.run(debug=True, host='0.0.0.0', port=5000)
