import os
import pickle
import numpy as np
import requests
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- Firebase Admin SDK Initialization ---
db = None
try:
    firebase_key = os.getenv("FIREBASE_KEY")
    if not firebase_key:
        raise ValueError("FIREBASE_KEY not found. Set it in Render environment variables.")

    cred = credentials.Certificate(json.loads(firebase_key))

    if not firebase_admin._apps:  # prevent re-init
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    print("Firestore initialized successfully.")
except Exception as e:
    print(f"Error initializing Firestore: {e}")

# --- API Key ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found.")

# --- Model Loading ---
model_path = os.path.join(os.path.dirname(__file__), "population.pickle4")
model = None
try:
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    print("ML Model loaded successfully.")
except FileNotFoundError:
    print(f"Error: ML Model file not found at {model_path}")
except Exception as e:
    print(f"An error occurred while loading the ML model: {e}")

# --- Frontend Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predictor")
def predictor():
    return render_template("population_predictor.html")



# --- API Routes ---
@app.route("/population_india", methods=["POST"])
def population_india():
    if not model:
        return jsonify({"error": "Machine learning model is not loaded."}), 500
    try:
        year = int(request.form["year"])
        if year < 2020:
            return jsonify({"error": "Please enter a year after 2020."}), 400

        year_array = np.array([[year]])
        predicted_population = model.predict(year_array)

        if not predicted_population.any():
            return jsonify({"error": "Model returned invalid prediction."}), 500

        return jsonify({"predicted_population": int(predicted_population[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat_proxy():
    try:
        user_payload = request.get_json()
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"
        response = requests.post(api_url, json=user_payload)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/analyze_population", methods=["POST"])
def analyze_population():
    try:
        data = request.get_json()
        year = data.get("year")
        population = data.get("population")

        if not year or not population:
            return jsonify({"error": "Year and population are required."}), 400

        prompt = f"Analyze India's socio-economic implications if population reaches {population} in {year}."

        payload = { "contents": [{ "parts": [{"text": prompt}] }] }
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/contact", methods=["POST"])
def handle_contact():
    if not db:
        return jsonify({"error": "Database not configured."}), 500
    try:
        data = request.get_json()
        if not all([data.get("name"), data.get("email"), data.get("message")]):
            return jsonify({"error": "All fields required."}), 400

        db.collection("submissions").add({
            "name": data["name"],
            "email": data["email"],
            "message": data["message"],
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        return jsonify({"success": "Message sent!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/freelance_request", methods=["POST"])
def handle_freelance_request():
    if not db:
        return jsonify({"error": "Database not configured."}), 500
    try:
        data = request.get_json()
        required = ["name", "mobile", "email", "work_type", "deadline", "client_type"]
        if not all(data.get(f) for f in required):
            return jsonify({"error": "Missing required fields."}), 400

        db.collection("freelance_requests").add({
            **data,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        return jsonify({"success": "Freelance request submitted!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/report_bug", methods=["POST"])
def handle_bug_report():
    if not db:
        return jsonify({"error": "Database not configured."}), 500
    try:
        data = request.get_json()
        required = ["name", "email", "mobile", "issue"]
        if not all(data.get(f) for f in required):
            return jsonify({"error": "Missing required fields."}), 400

        db.collection("bug_reports").add({
            **data,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        return jsonify({"success": "Bug reported!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)