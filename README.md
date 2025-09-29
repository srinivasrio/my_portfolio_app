Srinivas Kumar - Data Scientist & Python Developer Portfolio
This repository contains the complete source code for the personal portfolio website of Srinivas Kumar, a passionate Master of Computer Applications student with a specialization in Data Science and Python development. The website is a fully interactive, single-page application with a modern Glassmorphism design, built with a Flask backend and a dynamic frontend.


Features
This is a feature-rich web application designed to provide a comprehensive overview of my skills, experience, and projects.

Core Frontend Features:
Glassmorphism UI: A modern, beautiful user interface with frosted-glass effects and an animated, gradient background.

Dark/Light Mode: A theme switcher that allows users to toggle between a dark and light version of the website.

Fully Responsive: The layout is designed to work perfectly on all devices, from mobile phones to desktop computers.

Animated & Interactive Timeline: A visually engaging, scroll-animated timeline that details my academic and professional journey.

Dynamic Project Filtering: An interactive project gallery that can be filtered by category (Web Apps, Data Science) with smooth animations.

Interactive Modals: Clicking on projects or curriculum details opens up detailed information in beautiful, non-intrusive modal windows.

Certificate Lightbox: All certificates can be viewed in a high-quality, full-screen lightbox for easy viewing.

Backend & AI Integration:
Flask Backend: The website is powered by a robust and efficient Flask server.

Machine Learning Model Integration: Includes a live "Population Predictor" page that uses a Scikit-learn model (trained on historical data) to predict India's population.

Gemini API Chatbot: A fully integrated AI assistant that can answer visitor questions about my portfolio based on a specific, controlled context.

Gemini API for Analysis: The Population Predictor includes a feature to get an AI-generated socio-economic analysis of the prediction, using the Gemini API with Google Search grounding.

Firestore Database Integration: All forms on the website (Contact, Freelance Quote Request, and Bug Report) are connected to a Google Firestore database to securely save submissions.

Sections
Home: A welcoming hero section with a clear headline and a call-to-action.

About Me: A personal introduction detailing my passion for technology and data science.

My Journey: An interactive timeline of my educational and professional milestones, including clickable links and curriculum details.

Experience: A dedicated section for my internship experience, complete with a link to the certificate.

My Skills: A grid showcasing my technical skills, including programming languages, libraries, and tools.

My Projects: An interactive gallery of my work, which can be filtered by category.

Certifications & Achievements: A categorized display of my technical, academic, and school-level certificates.

Freelancing Services: A detailed section outlining the freelance services I offer, complete with a "Request a Quote" form.

Contact & Bug Report: A general contact form and a "Report a Bug" feature in the footer, both connected to the Firestore backend.

Technology Stack
Backend
Python

Flask: For the web server and API endpoints.

Firebase Admin SDK: To connect to the Firestore database.

Scikit-learn & NumPy: To load and run the machine learning model.

python-dotenv: For securely managing environment variables.

Frontend
HTML5

Tailwind CSS: For all styling and responsive design.

JavaScript: To handle all interactivity, including animations, API calls, and dynamic content rendering.

APIs & Services
Google Gemini API: Powers the AI chatbot and the population analysis feature.

Google Firestore: A NoSQL database used to store all form submissions.

How to Run Locally
To run this project on your own machine, please follow these steps:

Clone the repository:

git clone [https://github.com/srinivasrio/my_portfolio_app.git](https://github.com/srinivasrio/my_portfolio_app.git)
cd my_portfolio_app

Set up the virtual environment:

python3 -m venv venv
source venv/bin/activate

Install the dependencies:

pip install -r requirements.txt

Set up your secret keys:

Create a file named .env in the root folder and add your Gemini API key: GEMINI_API_KEY='YOUR_API_KEY'

Place your Google Cloud service account key file in the root folder and name it serviceAccountKey.json.

Run the application:

python3 app.py
