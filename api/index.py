import os
import firebase_admin
from firebase_admin import credentials

# Replace escaped newline strings with actual newlines
raw_key = os.getenv("FIREBASE_PRIVATE_KEY", "")
private_key = raw_key.replace("\\n", "\n")

if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key": private_key,
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    })
    firebase_admin.initialize_app(cred)