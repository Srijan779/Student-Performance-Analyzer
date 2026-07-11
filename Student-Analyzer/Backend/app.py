from flask import Flask
from flask_cors import CORS
import sys
import os

# Ensures Python can locate your database and analysis folders
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes import api_bp
from database.db import init_db

def create_app():
    app = Flask(__name__)
    
    # Allows the browser (Frontend) to talk to the server (Backend) securely
    CORS(app)
    
    # Registers the /predict and /search routes
    app.register_blueprint(api_bp, url_prefix='/api')

    # Creates the SQLite database file and tables on startup
    with app.app_context():
        try:
            init_db()
            print(">>> SUCCESS: Database initialized.")
        except Exception as e:
            print(f">>> ERROR: Database initialization failed. Details: {e}")

    return app

if __name__ == '__main__':
    my_app = create_app()
    print("Starting Full-Stack Server on http://127.0.0.1:5000")
    my_app.run(debug=True, port=5000)