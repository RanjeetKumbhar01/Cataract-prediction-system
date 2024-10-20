# firebase_config.py
import firebase_admin
from firebase_admin import credentials, db

def initialize_firebase():
    # Load the service account key from the JSON file
    cred = credentials.Certificate("static/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cataract-classification-system-default-rtdb.asia-southeast1.firebasedatabase.app/'  # Use your Firebase Realtime Database URL
        })