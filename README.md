Srinivas Kumar - AI Powered Portfolio ✨
Data Scientist & Python Developer
This repository contains the source code for my personal portfolio, a fully interactive, single-page application built to showcase my skills in Data Science and Python Development. The website features a stunning Glassmorphism design, a robust Flask backend, and is integrated with cutting-edge AI features powered by the Google Gemini API.

🎥 Live Demo & Preview
Check out the live website here: https://www.iamsrinivas.tech/


✨ Core Features
This isn't just a static page; it's a feature-rich web application designed to provide a comprehensive and interactive overview of my profile.

🎨 Frontend & UI
💎 Glassmorphism UI: A modern, beautiful user interface with frosted-glass effects and a fluid, animated gradient background.

🌓 Dark/Light Mode: A sleek theme switcher that allows users to toggle between dark and light modes, with their preference saved locally.

📱 Fully Responsive: The layout is meticulously designed to work perfectly on all devices, from mobile phones to widescreen desktops.

⏳ Animated Journey Timeline: A visually engaging, scroll-animated timeline that details my academic and professional journey.

📂 Dynamic Project Filtering: An interactive project gallery that can be filtered by category (Web Apps, Data Science) with smooth, fluid animations.

** modals:** Clicking on projects or curriculum details opens up detailed information in beautiful, non-intrusive modal windows.

📜 Certificate Lightbox: All certificates can be viewed in a high-quality, full-screen lightbox for clear and easy inspection.

🤖 Backend & AI Integration
🚀 Robust Flask Backend: The entire website is powered by a robust and efficient Python Flask server.

🧠 Live ML Model: A "Population Predictor" page that uses a live Scikit-learn model (trained on historical data) to predict India's future population.

💬 Gemini API Chatbot: A fully integrated AI assistant that can answer visitor questions about my skills, projects, and experience based on a controlled context.

📊 AI-Powered Analysis: The Population Predictor includes a feature to get a Gemini-generated socio-economic analysis of the prediction, grounded with Google Search.

💾 Firestore Database: All forms (Contact, Freelance Quote, Bug Report) are securely connected to a Google Firestore database to capture and store submissions in real-time.

🛠️ Technology Stack
This project was built using a modern and powerful stack, focusing on performance, scalability, and a great developer experience.

Category	Technologies & Tools
Backend	
Frontend	
APIs & Services	
Dev Tools & Others	

Export to Sheets
🚀 How to Run Locally
To get this project up and running on your local machine, follow these steps.

Prerequisites
Python 3.10+

Git

Installation & Setup
Clone the repository:

Bash

git clone https://github.com/srinivasrio/my_portfolio_app.git
cd my_portfolio_app
Create and activate a virtual environment:

Bash

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
Install the required dependencies:

Bash

pip install -r requirements.txt
Configure Environment Variables:
You'll need to set up your API keys and Firebase credentials. Create a file named .env in the root directory and add the following, replacing the placeholders with your actual credentials:

# .env.example
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
FIREBASE_TYPE="service_account"
FIREBASE_PROJECT_ID="your-firebase-project-id"
FIREBASE_PRIVATE_KEY_ID="your-firebase-private-key-id"
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_KEY_HERE\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL="your-firebase-client-email@..."
FIREBASE_CLIENT_ID="your-firebase-client-id"
FIREBASE_AUTH_URI="https://accounts.google.com/o/oauth2/auth"
FIREBASE_TOKEN_URI="https://oauth2.googleapis.com/token"
FIREBASE_AUTH_PROVIDER_X509_CERT_URL="https://www.googleapis.com/oauth2/v1/certs"
FIREBASE_CLIENT_X509_CERT_URL="your-cert-url"
Note: Your Firebase Private Key needs to be formatted correctly within the quotes to handle newlines.

Run the Flask application:

Bash

python3 app.py
The application will be running at http://127.0.0.1:5000.
