# firebase_config.py
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    # Load the service account key from the JSON file
    cred = credentials.Certificate("static/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
