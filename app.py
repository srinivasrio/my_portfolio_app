import os
import json
import pickle
import pathlib
import numpy as np
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Resolve absolute project directory to avoid TemplateNotFound on Render
BASE_DIR = pathlib.Path(__file__).parent.resolve()

# If HTML files are at repo root, point template_folder to BASE_DIR.
# If you later move them into /templates, change to app = Flask(__name__) and put files there.
app = Flask(__name__, template_folder=str(BASE_DIR))
CORS(app)

# ---------- Firebase Admin SDK Initialization ----------
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

# ---------- External API Keys ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found. /api/chat and /api/analyze_population will fail.")

# ---------- ML Model Loading (robust) ----------
MODEL_PATH_ENV = os.getenv("MODEL_PATH")  # optional explicit path
MODEL_URL = os.getenv("MODEL_URL")        # optional download URL at startup

MODEL = None
MODEL_LOAD_ERR = None

def download_model_if_needed():
    """
    Optional: download model from MODEL_URL to MODEL_PATH_ENV or default path if not present.
    """
    try:
        if not MODEL_URL:
            return
        target = MODEL_PATH_ENV or str(BASE_DIR / "population.pickle4")
        if os.path.exists(target):
            return
        print(f"Downloading model from {MODEL_URL} ...")
        r = requests.get(MODEL_URL, timeout=60)
        r.raise_for_status()
        with open(target, "wb") as f:
            f.write(r.content)
        print(f"Model downloaded to {target}")
    except Exception as e:
        print(f"Warning: could not download model: {e}")

def load_model_once():
    """
    Load the ML model from multiple possible locations, once per process.
    """
    global MODEL, MODEL_LOAD_ERR
    if MODEL is not None or MODEL_LOAD_ERR is not None:
        return
    try:
        candidates = []
        if MODEL_PATH_ENV:
            candidates.append(MODEL_PATH_ENV)
        # Try your current name first, then common alternates
        candidates += [
            str(BASE_DIR / "population.pickle4"),  # your new file
            str(BASE_DIR / "population.pickle"),   # older/newer alt
            str(BASE_DIR / "population.pickle3"),  # older alt
            str(BASE_DIR / "population.pkl"),      # common alt
        ]

        last_err = None
        for p in candidates:
            try:
                if os.path.exists(p):
                    with open(p, "rb") as f:
                        MODEL = pickle.load(f)
                    print(f"ML model loaded from: {p}")
                    return
            except Exception as e:
                last_err = e
        if MODEL is None:
            raise FileNotFoundError(f"Model not found. Tried: {candidates}. Last error: {last_err}")
    except Exception as e:
        MODEL_LOAD_ERR = str(e)
        print(f"Error loading ML model: {MODEL_LOAD_ERR}")

# Optional: fetch the model file if hosted remotely
download_model_if_needed()
# Load the model now (once)
load_model_once()

# ---------- Frontend Routes ----------
@app.route("/")
def home():
    # index.html is expected in BASE_DIR (repo root) given template_folder str(BASE_DIR)
    return render_template("index.html")

@app.route("/predictor")
def predictor():
    # population_predictor.html is expected in BASE_DIR
    return render_template("population_predictor.html")

@app.route("/freelancing")
def freelancing():
    # If you don't have freelancing.html yet, comment this route or add the file to BASE_DIR.
    return render_template("freelancing.html")

# ---------- API: ML Predictor ----------
@app.route("/population_india", methods=["POST"])
def population_india():
    # Ensure model is attempted again if initial load failed due to race
    load_model_once()
    if MODEL is None:
        return jsonify({"error": "Machine learning model is not loaded.", "detail": MODEL_LOAD_ERR}), 500

    try:
        # Accept both classic form data and JSON
        data = request.get_json(silent=True) or {}
        year_val = request.form.get("year") or data.get("year")
        if year_val is None or str(year_val).strip() == "":
            return jsonify({"error": "Missing 'year'"}), 400

        year = int(year_val)
        if year < 2020:
            return jsonify({"error": "Please enter a year after 2020."}), 400

        # Input to model as 2D array for scikit-learn
        X = np.array([[year]], dtype=float)
        y_pred = MODEL.predict(X)

        # Safety checks
        if y_pred is None or len(y_pred) == 0:
            return jsonify({"error": "Model returned no prediction."}), 500

        # Coerce to int if regression returns float
        try:
            value = int(round(float(y_pred[0])))
        except Exception:
            value = y_pred[0]

        return jsonify({"predicted_population": value})
    except ValueError:
        return jsonify({"error": "Year must be a number."}), 400
    except Exception as e:
        # Log server-side
        print(f"/population_india error: {e}")
        return jsonify({"error": str(e)}), 500

# ---------- API: Gemini proxy ----------
@app.route("/api/chat", methods=["POST"])
def chat_proxy():
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY not configured"}), 500
    try:
        user_payload = request.get_json(force=True)
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"
        response = requests.post(api_url, json=user_payload, timeout=60)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        print(f"/api/chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/analyze_population", methods=["POST"])
def analyze_population():
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY not configured"}), 500
    try:
        data = request.get_json(force=True)
        year = data.get("year")
        population = data.get("population")

        if not year or not population:
            return jsonify({"error": "Year and population are required."}), 400

        prompt = f"Analyze India's socio-economic implications if population reaches {population} in {year}."
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"
        response = requests.post(api_url, json=payload, timeout=60)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        print(f"/api/analyze_population error: {e}")
        return jsonify({"error": str(e)}), 500

# ---------- API: Forms to Firestore ----------
@app.route("/contact", methods=["POST"])
def handle_contact():
    if not db:
        return jsonify({"error": "Database not configured."}), 500
    try:
        data = request.get_json(force=True)
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
        print(f"/contact error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/freelance_request", methods=["POST"])
def handle_freelance_request():
    if not db:
        return jsonify({"error": "Database not configured."}), 500
    try:
        data = request.get_json(force=True)
        required = ["name", "mobile", "email", "work_type", "deadline", "client_type"]
        if not all(data.get(f) for f in required):
            return jsonify({"error": "Missing required fields."}), 400
        db.collection("freelance_requests").add({
            **data,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        return jsonify({"success": "Freelance request submitted!"})
    except Exception as e:
        print(f"/freelance_request error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/report_bug", methods=["POST"])
def handle_bug_report():
    if not db:
        return jsonify({"error": "Database not configured."}), 500
    try:
        data = request.get_json(force=True)
        required = ["name", "email", "mobile", "issue"]
        if not all(data.get(f) for f in required):
            return jsonify({"error": "Missing required fields."}), 400
        db.collection("bug_reports").add({
            **data,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        return jsonify({"success": "Bug reported!"})
    except Exception as e:
        print(f"/report_bug error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # For local dev only; on Render use gunicorn:
    # gunicorn app:app -b 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
