import os
import vertexai
from vertexai.generative_models import GenerativeModel
from flask import Flask, request, jsonify

app = Flask(__name__)

# Config
PROJECT_ID = "guardian-proxy-hackathon" 
LOCATION = "us-central1" 

print(f"Connecting to Vertex AI Project: {PROJECT_ID}...")
vertexai.init(project=PROJECT_ID, location=LOCATION)

model = GenerativeModel("gemini-2.5-flash")

@app.route('/', methods=['GET'])
def health_check():
    """Simple check to see if server is running."""
    return "Guardian Proxy is Active!", 200

@app.route('/chat', methods=['POST'])
def chat():
    """Receives a prompt, sends to Gemini, returns response."""
    try:
        data = request.json
        user_prompt = data.get('prompt')

        if not user_prompt:
            return jsonify({"error": "No prompt provided"}), 400

        print(f"Received prompt: {user_prompt}")
        
        response = model.generate_content(user_prompt)
        
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)