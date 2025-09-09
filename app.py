import os
import pickle
import numpy as np
import requests
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app)

# --- Firebase Admin SDK Initialization ---
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firestore initialized successfully.")
except Exception as e:
    db = None
    print(f"Error initializing Firestore: {e}")
    print("Could not connect to the database. Please ensure 'serviceAccountKey.json' is present and correct.")

# --- API Key ---
GEMINI_API_KEY = 'AIzaSyAxUSJ6427XJqUyLwxytskuynVmQmjH-Q4'

# --- Model Loading ---
model_path = os.path.join(os.path.dirname(__file__), 'population.pickle3')
model = None
try:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    print("ML Model loaded successfully.")
except FileNotFoundError:
    print(f"Error: ML Model file not found at {model_path}")
except Exception as e:
    print(f"An error occurred while loading the ML model: {e}")

# --- Frontend Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predictor')
def predictor():
    return render_template('population_predictor.html')

# --- API Routes ---
@app.route('/population_india', methods=['POST'])
def population_india():
    if not model:
        return jsonify({'error': 'Machine learning model is not loaded.'}), 500
    try:
        year = int(request.form['year'])
        if year < 2020:
            return jsonify({'error': 'Please enter a year after 2020.'}), 400

        year_array = np.array([[year]])
        predicted_population = model.predict(year_array)
        
        if predicted_population is None or len(predicted_population) == 0 or not np.isfinite(predicted_population[0]):
             return jsonify({'error': 'Model returned an invalid prediction.'}), 500

        int_prediction = int(predicted_population[0])
        return jsonify({'predicted_population': int_prediction})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    try:
        user_payload = request.get_json()
        api_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}'
        
        response = requests.post(api_url, json=user_payload)
        response.raise_for_status()
        
        return jsonify(response.json())
    except Exception as e:
        print(f"Chat Proxy Error: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

@app.route('/contact', methods=['POST'])
def handle_contact():
    if not db:
         return jsonify({'error': 'Database is not configured correctly.'}), 500
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not name or not email or not message:
            return jsonify({'error': 'All fields are required.'}), 400

        doc_ref = db.collection('submissions').document()
        doc_ref.set({
            'name': name,
            'email': email,
            'message': message,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        
        print("--- New Contact Form Submission Saved to Firestore ---")
        
        return jsonify({'success': 'Your message has been sent successfully!'})
    except Exception as e:
        print(f"Contact form error: {e}")
        return jsonify({'error': 'An error occurred on the server.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

