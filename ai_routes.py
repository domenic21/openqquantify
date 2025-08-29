from flask import Blueprint, request, jsonify , render_template
from openai_service import get_quantum_insight
from arxiv_fetcher import fetch_arxiv_data, cache_arxiv_data
from datetime import datetime

ai_routes = Blueprint('ai_routes', __name__) #blueprint is a way to organize your Flask application into modules, allowing you to group related routes and functionality together.
#post quantum insights using a POST request
@ai_routes.route('/api/quantum', methods=['POST'])
def generate_quantum_info():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    response = get_quantum_insight(prompt)
    return jsonify({"response": response})

# Get quantum insights using a GET request 
@ai_routes.route('/api/quantum', methods=['GET'])
def get_quantum_info():
    prompt = request.args.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    response = get_quantum_insight(prompt)
    return jsonify({"response": response})

@ai_routes.route("/")
def index():
    arxiv_entries = fetch_arxiv_data(max_results=6)
    return render_template("index.html", arxiv_entries=arxiv_entries, last_updated=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))